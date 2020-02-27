package eu.me2d.cmlmobile

import android.app.Application
import com.jakewharton.threetenabp.AndroidThreeTen
import timber.log.Timber
import timber.log.Timber.DebugTree


class CmlMobileApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        AndroidThreeTen.init(this);
        if (BuildConfig.DEBUG) {
            Timber.plant(DebugTree())
        }
    }
}