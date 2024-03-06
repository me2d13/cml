package eu.me2d.cmlmobile.car

import android.content.Intent
import androidx.car.app.Screen
import androidx.car.app.Session
import eu.me2d.cmlmobile.HistoryService
import eu.me2d.cmlmobile.PersistenceService
import eu.me2d.cmlmobile.api.ApiService

class CmlCarSession : Session() {
    override fun onCreateScreen(intent: Intent): Screen {
        val persistenceService = PersistenceService(carContext)
        val historyService = HistoryService()
        val storedData = persistenceService.loadAll()
        historyService.initHistory(storedData.history)
        val commands = historyService.sortCommands(storedData.commands)
        val apiService = if (storedData.url != null && storedData.privateKeyString != null)
            ApiService(storedData.url!!, storedData.privateKeyString!!)
        else
            null
        return MainCmlCarScreen(carContext, commands) { commandClickedNum ->
            apiService?.let {
                it.executeCommand(commandClickedNum)
                historyService.commandExecuted(commandClickedNum)
                persistenceService.saveHistory(historyService.historyForLastNDays(10))
            }
        }
    }
}