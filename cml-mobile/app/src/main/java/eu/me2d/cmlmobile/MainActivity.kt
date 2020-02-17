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
    }
}
