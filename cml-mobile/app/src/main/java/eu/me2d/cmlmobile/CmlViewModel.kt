package eu.me2d.cmlmobile

import android.app.Application
import androidx.lifecycle.*
import androidx.preference.PreferenceManager
import timber.log.Timber
import java.security.Key
import java.security.KeyPair
import java.security.KeyPairGenerator
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.time.format.FormatStyle
import java.util.*
import javax.crypto.spec.SecretKeySpec

class CmlViewModel(application: Application) : AndroidViewModel(application) {

    companion object Keys {
        const val KEY_SERVER_URL = "serverUrl"
        const val KEY_SENT_DATE = "sentDate"
        const val KEY_PRIVATE_KEY = "privateKey"
    }

    val url: MutableLiveData<String>
    private val sentDate: MutableLiveData<LocalDateTime>
    val sentDateString: LiveData<String>
    private var privateKey: Key? = null

    init {
        Timber.d("Reading state from shared props")
        val sharedPrefs = PreferenceManager.getDefaultSharedPreferences(application)
        url = MutableLiveData(sharedPrefs.getString(KEY_SERVER_URL, "https://"))
        val sendDateString = sharedPrefs.getString(KEY_SENT_DATE, null)
        sentDate = MutableLiveData<LocalDateTime>(if (sendDateString == null) null else LocalDateTime.parse(sendDateString))
        sentDateString = Transformations.map(sentDate) {it?.format(DateTimeFormatter.ofLocalizedDateTime(FormatStyle.SHORT)) ?: "Not yet sent"}
        val privateKeyString = sharedPrefs.getString(KEY_PRIVATE_KEY, null)
        if (privateKeyString != null) {
            val decodedKey = Base64.getDecoder().decode(privateKeyString)
            privateKey = SecretKeySpec(decodedKey, "RSA")
        }
    }


    fun onSendRequest() {
        val kpg: KeyPairGenerator = KeyPairGenerator.getInstance("RSA")
        kpg.initialize(2048)
        val kp: KeyPair = kpg.generateKeyPair()
        privateKey = kp.private
        val pub: Key = kp.public
        val encoder: Base64.Encoder = Base64.getEncoder()
        val publicKey = encoder.encodeToString(pub.encoded)
        val publicKeyStr = "-----BEGIN RSA PUBLIC KEY-----\n${publicKey}\n-----END RSA PUBLIC KEY-----\n"
        Timber.i("Sending request to %s", url.value)
        Timber.i("Public key is %s", publicKeyStr)
        sentDate.value = LocalDateTime.now()
        saveToSharedPrefs()
    }

    private fun saveToSharedPrefs() {
        val sharedPrefs = PreferenceManager.getDefaultSharedPreferences(getApplication())
        with (sharedPrefs.edit()) {
            putString(KEY_SERVER_URL, url.value)
            if (sentDate.value != null) {
                putString(KEY_SENT_DATE, sentDate.value.toString())
            }
            if (privateKey != null) {
                putString(KEY_PRIVATE_KEY, Base64.getEncoder().encodeToString(privateKey!!.encoded))
            }
            commit()
        }
    }
}