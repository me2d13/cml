package eu.me2d.cmlmobile

import android.os.Build
import androidx.annotation.RequiresApi
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.Transformations
import androidx.lifecycle.ViewModel
import timber.log.Timber
import java.security.Key
import java.security.KeyPair
import java.security.KeyPairGenerator
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.time.format.FormatStyle
import java.util.*

class CmlViewModel: ViewModel() {

    val url: MutableLiveData<String> = MutableLiveData("https://")
    val sentDate: MutableLiveData<LocalDateTime> = MutableLiveData<LocalDateTime>(null)
    @RequiresApi(Build.VERSION_CODES.O)
    val sentDateString = Transformations.map(sentDate) {it?.format(DateTimeFormatter.ofLocalizedDateTime(FormatStyle.SHORT)) ?: "Not yet sent"}

    @RequiresApi(Build.VERSION_CODES.O)
    fun onSendRequest() {
        val kpg: KeyPairGenerator = KeyPairGenerator.getInstance("RSA")
        kpg.initialize(2048)
        val kp: KeyPair = kpg.generateKeyPair()
        val pvt: Key = kp.private
        val pub: Key = kp.public
        val encoder: Base64.Encoder = Base64.getEncoder()
        val publicKey = encoder.encodeToString(pub.encoded)
        val publicKeyStr = "-----BEGIN RSA PUBLIC KEY-----\n${publicKey}\n-----END RSA PUBLIC KEY-----\n"
        Timber.i("Sending request to %s", url.value)
        Timber.i("Public key is %s", publicKeyStr)
        sentDate.value = LocalDateTime.now()
        //TODO: save private key, url and date to shared prefs
    }
}