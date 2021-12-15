package eu.me2d.cmlmobile

import android.app.Application
import androidx.preference.PreferenceManager
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import eu.me2d.cmlmobile.api.Command
import org.threeten.bp.LocalDateTime
import timber.log.Timber

class PersistenceService(private val application: Application) {

    companion object Keys {
        const val KEY_SERVER_URL = "serverUrl"
        const val KEY_SENT_DATE = "sentDate"
        const val KEY_PRIVATE_KEY = "privateKey"
        const val KEY_CURRENT_TAB = "currentTab"
        const val KEY_COMMANDS = "commands"
    }

    private val sharedPrefs = PreferenceManager.getDefaultSharedPreferences(application)
    private val gson = Gson()

    fun loadAll(): PersistedData {
        val sendDateString = sharedPrefs.getString(KEY_SENT_DATE, null)
        val commandsString = sharedPrefs.getString(KEY_COMMANDS, "[]")
        val sType = object : TypeToken<List<Command>>() { }.type
        return PersistedData(
            sharedPrefs.getString(KEY_SERVER_URL, "https://") ?: "https://",
            if (sendDateString == null) null else LocalDateTime.parse(sendDateString),
            sharedPrefs.getString(KEY_PRIVATE_KEY, null),
            sharedPrefs.getInt(KEY_CURRENT_TAB, 0),
            //gson.fromJson(commandsString, sType)
        listOf(Command(91, "Otevrit branu zahrady asi tak na jednu minutu plus minus"), Command(2, "Com2"))
        )
    }

    fun saveAll(data: PersistedData) {
        val sharedPrefs = PreferenceManager.getDefaultSharedPreferences(application)
        with (sharedPrefs.edit()) {
            putString(KEY_SERVER_URL, data.url)
            if (data.sent != null) {
                putString(KEY_SENT_DATE, data.sent.toString())
            }
            if (data.privateKeyString != null) {
                putString(KEY_PRIVATE_KEY, data.privateKeyString)
            }
            putInt(KEY_CURRENT_TAB, data.currentTab)
            putString(KEY_COMMANDS, gson.toJson(data.commands))
            commit()
        }
    }

    fun saveCurrentTab(value: Int) {
        Timber.d("Storing current tab %d", value)
        with(sharedPrefs.edit()) {
            putInt(KEY_CURRENT_TAB, value)
            commit()
        }
    }



}

data class PersistedData(
    var url: String?,
    var sent: LocalDateTime?,
    var privateKeyString: String?,
    var currentTab: Int,
    var commands: List<Command>,
)