package eu.me2d.cmlmobile

import android.app.Application
import timber.log.Timber
import timber.log.Timber.DebugTree


class CmlMobileApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        if (BuildConfig.DEBUG) {
            Timber.plant(DebugTree())
        }
    }
}