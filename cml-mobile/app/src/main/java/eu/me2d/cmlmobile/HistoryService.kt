package eu.me2d.cmlmobile

import android.annotation.SuppressLint
import eu.me2d.cmlmobile.api.Command
import java.text.SimpleDateFormat
import java.util.*
import kotlin.collections.HashMap

class HistoryService {
    var history: MutableMap<String, MutableMap<Int, Int>> = HashMap()
    @SuppressLint("SimpleDateFormat")
    private val sdf = SimpleDateFormat("yyyy-MM-dd")

    fun commandExecuted(commandNumber: Int, onDate: Date = Date()) {
        val dateKey = sdf.format(onDate)
        val commandsForDay = history.getOrPut(dateKey) {HashMap()}
        val commandValue = commandsForDay.getOrPut(commandNumber) {0}
        commandsForDay[commandNumber] = commandValue + 1
    }

    fun historyForLastNDays(numberOfDays: Int) : Map<String, Map<Int, Int>> {
        val actualKeys = history.keys.sorted().reversed().take(numberOfDays)
        return history.filterKeys { actualKeys.contains(it) }
    }

    fun commandsOrder() : List<Int> {
        val totals = HashMap<Int, Int>()
        history.values.forEach { dayMap ->
            dayMap.forEach {
                val current = totals.getOrPut(it.key) {0}
                totals[it.key] = current + it.value
            }
        }
        return totals.keys.sortedBy { totals[it] }.reversed()
    }

    fun sortCommands(commands: List<Command>): List<Command> {
        val result = ArrayList<Command>(commands.size)
        val commandsMap = commands.associateBy { it.number }
        val history = commandsOrder()
        history.forEach { commandNumber ->
            val command = commandsMap.get(commandNumber)
            command?.let { result.add(it) }
        }
        result.addAll(commands.filterNot { history.contains(it.number) })
        return result
    }

    fun initHistory(value: Map<String, Map<Int, Int>>) {
        history.clear()
        value.forEach { (k, v) -> history[k] = v.toMutableMap() }
    }
}