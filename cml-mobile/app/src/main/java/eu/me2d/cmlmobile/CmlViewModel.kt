package eu.me2d.cmlmobile

import android.app.Application
import android.util.Base64
import androidx.lifecycle.*
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

    private lateinit var apiService: ApiService
    private var persistenceService = PersistenceService(application)
    var historyService = HistoryService()

    val url: MutableLiveData<String>
    val note: MutableLiveData<String> = MutableLiveData("")
    private val sentDate: MutableLiveData<LocalDateTime>
    val sentDateString: LiveData<String>
    private var privateKey: PrivateKey? = null
    val sentResult: MutableLiveData<String> = MutableLiveData()
    val commands: MutableLiveData<List<Command>> = MutableLiveData()
    val commandsString: LiveData<String>
    val paired: LiveData<Boolean>
    val toastCode: MutableLiveData<Int> = MutableLiveData()
    var currentTab: Int = 0
        set(value) {
            field = value
            persistenceService.saveCurrentTab(value)
        }

    init {
        val storedData = persistenceService.loadAll()
        historyService.initHistory(storedData.history)
        commands.value = storedData.commands
        url = MutableLiveData(storedData.url)
        sentDate = MutableLiveData<LocalDateTime>(storedData.sent)
        sentDateString = Transformations.map(sentDate) {
            it?.format(
                DateTimeFormatter.ofLocalizedDateTime(
                    FormatStyle.SHORT
                )
            ) ?: "Not yet sent"
        }
        commandsString = Transformations.map(commands) {
            it.stream().map { c -> "%2d: %s".format(c.number, c.description) }
                .collect(Collectors.joining("\n"))
        }
        if (storedData.privateKeyString != null) {
            val decodedKey = Base64.decode(storedData.privateKeyString, Base64.DEFAULT)
            val kf: KeyFactory = KeyFactory.getInstance("RSA")
            privateKey = kf.generatePrivate(PKCS8EncodedKeySpec(decodedKey))
        }
        if (!url.value.isNullOrEmpty() && privateKey != null) {
            try {
                apiService = ApiService(url.value!!, privateKey!!)
            } catch (e: RuntimeException) {
                Timber.e(e, "Error creating API service")
            }
        }
        paired = MediatorLiveData()
        paired.addSource(url) { paired.value = haveInfoForApiCalls() }
        paired.addSource(sentDate) { paired.value = haveInfoForApiCalls() }
        currentTab = storedData.currentTab
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
        //Timber.i("Private key is %s", Base64.encodeToString(privateKey!!.encoded, Base64.DEFAULT))
        sentDate.value = LocalDateTime.now()
        saveToSharedPrefs()
        if (url.value != null && privateKey != null) {
            try {
                apiService = ApiService(url.value!!, privateKey!!)
                apiService.register(publicKeyStr, note.value, sentResult)
            } catch (e: RuntimeException) {
                Timber.e(e, "Error sending register request")
                sentResult.value = "Error: ${e.message}"
            }
        }
    }

    fun fetchCommands() {
        if (haveInfoForApiCalls()) {
            apiService.fetchCommands(commands, toastCode) { saveToSharedPrefs() }
        } else {
            Timber.w("Can't fetch commands, register client first")
        }
    }

    fun executeCommand(number: Number) {
        if (haveInfoForApiCalls()) {
            apiService.executeCommand(number)
            historyService.commandExecuted(number.toInt())
            persistenceService.saveHistory(historyService.historyForLastNDays(10))
        } else {
            Timber.w("Can't execute command, register client first")
        }
    }

    private fun haveInfoForApiCalls(): Boolean {
        return !url.value.isNullOrEmpty() && sentDate.value != null && privateKey != null
    }

    private fun saveToSharedPrefs() {
        persistenceService.saveAll(
            PersistedData(
                url = url.value,
                sent = sentDate.value,
                privateKeyString = if (privateKey == null) null else Base64.encodeToString(
                    privateKey!!.encoded, Base64.DEFAULT
                ),
                currentTab = currentTab,
                commands = commands.value ?: emptyList(),
                history = historyService.historyForLastNDays(10)
            )
        )
    }
}