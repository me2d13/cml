package eu.me2d.cmlmobile

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.NavController
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.fragment.findNavController
import eu.me2d.cmlmobile.databinding.ActivityMainBinding


class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var navController: NavController

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        binding.apply {
            setContentView(root)

            // find nav controller
            val navHostFragment = supportFragmentManager.findFragmentById(R.id.nav_host_fragment) as NavHostFragment
            navController = navHostFragment.findNavController()

            // hide back button from top level fragments
            //appBarConfiguration = AppBarConfiguration(setOf(R.id.homeFragment, R.id.searchFragment), binding.drawerLayout)

            setSupportActionBar(toolbar)
            //setupActionBarWithNavController(navController, appBarConfiguration)

            //bottomNavigation.setupWithNavController(navController)
            //navigationDrawer.setupWithNavController(navController)

/*
            // hide bottom navigation
            navController.addOnDestinationChangedListener { _, destination, _ ->
                when (destination.id) {
                    R.id.termsFragment, R.id.settingsFragment ->
                        bottomNavigation.visibility = View.GONE
                    else ->
                        bottomNavigation.visibility = View.VISIBLE
                }
            }
*/
        }
    }

}
