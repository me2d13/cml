package eu.me2d.cmlmobile

import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.ui.AppBarConfiguration
import com.google.android.material.snackbar.Snackbar
import eu.me2d.cmlmobile.databinding.ActivityMainBinding
import io.jsonwebtoken.Jwts
import timber.log.Timber
import java.security.Key
import java.security.KeyPair
import java.security.KeyPairGenerator
import java.util.*


class MainActivity : AppCompatActivity() {

    //private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        //binding = ActivityMainBinding.inflate(layoutInflater)
        setSupportActionBar(findViewById(R.id.toolbar))

/*
        fab.setOnClickListener { view ->
            val kpg: KeyPairGenerator = KeyPairGenerator.getInstance("RSA")
            kpg.initialize(2048)
            val kp: KeyPair = kpg.generateKeyPair()
            val pvt: Key = kp.private
            val pub: Key = kp.public
            val jws = Jwts.builder()
                .setSubject("Bob")
                .signWith(pvt)
                .compact()
            Timber.i("JWS is %s", jws)
            val encoder: Base64.Encoder = Base64.getEncoder()
            val publicKey = encoder.encodeToString(pub.encoded)
            val publicKeyStr = "-----BEGIN RSA PUBLIC KEY-----\n${publicKey}\n-----END RSA PUBLIC KEY-----\n"
            Timber.i("Public key is %s", publicKeyStr)


            Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                .setAction("Action", null).show()
        }
*/

    }
}
