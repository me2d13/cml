package eu.me2d.cmlmobile

import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.snackbar.Snackbar
import io.jsonwebtoken.Jwts
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.content_main.*
import timber.log.Timber
import java.security.Key
import java.security.KeyPair
import java.security.KeyPairGenerator
import java.util.*


class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(toolbar)

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

        b1.setOnClickListener { v -> this.onClick(v)}
        b2.setOnClickListener { v -> this.onClick(v)}
        b3.setOnClickListener { v -> this.onClick(v)}
        b4.setOnClickListener { v -> this.onClick(v)}
        b5.setOnClickListener { v -> this.onClick(v)}
        b6.setOnClickListener { v -> this.onClick(v)}
        b7.setOnClickListener { v -> this.onClick(v)}
        b8.setOnClickListener { v -> this.onClick(v)}
        b9.setOnClickListener { v -> this.onClick(v)}
        b0.setOnClickListener { v -> this.onClick(v)}
        bc.setOnClickListener { input.text = ""}
    }

    private fun onClick(v: View) {
        val button: Button = v as Button
        input.text = String.format("%s%s", input.text, button.text)
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        return when (item.itemId) {
            R.id.action_settings -> true
            else -> super.onOptionsItemSelected(item)
        }
    }
}
