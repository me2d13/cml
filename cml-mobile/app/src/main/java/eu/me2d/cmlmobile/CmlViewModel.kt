package eu.me2d.cmlmobile

import android.app.Application
import android.util.Base64
import androidx.lifecycle.*
import androidx.preference.PreferenceManager
import eu.me2d.cmlmobile.api.ApiService
import eu.me2d.cmlmobile.api.Command
import org.threeten.bp.LocalDateTime
import org.threeten.bp.format.DateTimeFormatter
import org.threeten.bp.format.FormatStyle
import timber.log.Timber
import java.security.*
import java.security.spec.PKCS8EncodedKeySpec
import java.util.stream.Collectors

class CmlViewModel(application: Application) : AndroidViewModel(application) {

    companion object Keys {
        const val KEY_SERVER_URL = "serverUrl"
        const val KEY_SENT_DATE = "sentDate"
        const val KEY_PRIVATE_KEY = "privateKey"
    }

    val url: MutableLiveData<String>
    val note: MutableLiveData<String> = MutableLiveData("")
    private val sentDate: MutableLiveData<LocalDateTime>
    val sentDateString: LiveData<String>
    private var privateKey: PrivateKey? = null
    private var apiService: ApiService? = null
    val sentResult: MutableLiveData<String> = MutableLiveData()
    private val commands: MutableLiveData<List<Command>> = MutableLiveData()
    val commandsString: LiveData<String>
    val paired: LiveData<Boolean>
    val toastCode: MutableLiveData<Int> = MutableLiveData()

    init {
        Timber.d("Reading state from shared props")
        val sharedPrefs = PreferenceManager.getDefaultSharedPreferences(application)
        url = MutableLiveData(sharedPrefs.getString(KEY_SERVER_URL, "https://"))
        val sendDateString = sharedPrefs.getString(KEY_SENT_DATE, null)
        sentDate = MutableLiveData<LocalDateTime>(if (sendDateString == null) null else LocalDateTime.parse(sendDateString))
        sentDateString = Transformations.map(sentDate) {it?.format(
            DateTimeFormatter.ofLocalizedDateTime(
            FormatStyle.SHORT)) ?: "Not yet sent"}
        commandsString = Transformations.map(commands) {it.stream().map { c -> "%2d: %s".format(c.number, c.description) }
            .collect(Collectors.joining("\n"))}
        val privateKeyString = sharedPrefs.getString(KEY_PRIVATE_KEY, null)
        //Timber.i("Private key from shared prefs is %s", privateKeyString)
        if (privateKeyString != null) {
            val decodedKey = Base64.decode(privateKeyString, Base64.DEFAULT)
            val kf: KeyFactory = KeyFactory.getInstance("RSA")
            privateKey = kf.generatePrivate(PKCS8EncodedKeySpec(decodedKey))
        }
        if (!url.value.isNullOrEmpty() && privateKey != null) {
            apiService = ApiService(url.value!!, privateKey!!)
        }
        paired = MediatorLiveData<Boolean>()
        paired.addSource(url) { paired.value = haveInfoForApiCalls() }
        paired.addSource(sentDate) { paired.value = haveInfoForApiCalls() }
    }


    fun sendRegisterClientRequest() {
        val kpg: KeyPairGenerator = KeyPairGenerator.getInstance("RSA")
        kpg.initialize(2048)
        val kp: KeyPair = kpg.generateKeyPair()
        privateKey = kp.private
        val pub: Key = kp.public
        val publicKey = Base64.encodeToString(pub.encoded, Base64.DEFAULT)
        val publicKeyStr = "-----BEGIN PUBLIC KEY-----\n${publicKey}-----END PUBLIC KEY-----\n"
        Timber.i("Sending request to %s", url.value)
        Timber.i("Public key is %s", publicKeyStr)
        Timber.i("Private key is %s", Base64.encodeToString(privateKey!!.encoded, Base64.DEFAULT))
        sentDate.value = LocalDateTime.now()
        saveToSharedPrefs()
        if (url.value != null && privateKey != null) {
            apiService = ApiService(url.value!!, privateKey!!)
            apiService?.register(publicKeyStr, note.value, sentResult)
        }
    }

    fun fetchCommands() {
        if (haveInfoForApiCalls()) {
            apiService?.fetchCommands(commands, toastCode)
        } else {
            Timber.w("Can't fetch commands, register client first")
        }
    }

    fun executeCommand(number: Number) {
        if (haveInfoForApiCalls()) {
            apiService?.executeCommand(number)
        } else {
            Timber.w("Can't execute command, register client first")
        }
    }

    private fun haveInfoForApiCalls(): Boolean {
        return !url.value.isNullOrEmpty() && sentDate.value != null && privateKey != null
    }

    private fun saveToSharedPrefs() {
        val sharedPrefs = PreferenceManager.getDefaultSharedPreferences(getApplication())
        with (sharedPrefs.edit()) {
            putString(KEY_SERVER_URL, url.value)
            if (sentDate.value != null) {
                putString(KEY_SENT_DATE, sentDate.value.toString())
            }
            if (privateKey != null) {
                putString(KEY_PRIVATE_KEY, Base64.encodeToString(privateKey!!.encoded, Base64.DEFAULT))
            }
            commit()
        }
    }
}