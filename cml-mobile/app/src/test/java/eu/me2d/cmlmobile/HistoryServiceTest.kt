package eu.me2d.cmlmobile

import com.google.gson.Gson
import eu.me2d.cmlmobile.api.Command
import junit.framework.TestCase
import org.junit.Assert
import java.text.SimpleDateFormat
import java.util.*

class HistoryServiceTest : TestCase() {

    fun testCommandExecuted() {
        val cut = HistoryService()
        cut.commandExecuted(1)
        Assert.assertEquals(1, cut.history.size)
    }

    fun dt(value: String) = SimpleDateFormat("yyyy-MM-dd").parse(value) ?: Date()

    fun testHistoryForLastNDays() {
        val cut = HistoryService()
        cut.commandExecuted(3, dt("2020-01-01"))
        cut.commandExecuted(1, dt("2020-01-01"))
        cut.commandExecuted(1, dt("2020-01-02"))
        cut.commandExecuted(2, dt("2020-02-02"))
        Assert.assertEquals(3, cut.history.size)
        val last2 = cut.historyForLastNDays(2)
        Assert.assertEquals(2, last2.size)
        Assert.assertTrue(last2.keys.contains("2020-01-02"))
        Assert.assertTrue(last2.keys.contains("2020-02-02"))
    }

    fun testSorting() {
        val cut = HistoryService()
        cut.commandExecuted(1)
        cut.commandExecuted(2, dt("2008-01-02"))
        cut.commandExecuted(2)
        cut.commandExecuted(3)
        cut.commandExecuted(3, dt("2020-01-02"))
        cut.commandExecuted(3)
        val commands = cut.commandsOrder()
        Assert.assertEquals(3, commands.size)
        Assert.assertEquals(3, commands[0])
        Assert.assertEquals(2, commands[1])
        Assert.assertEquals(1, commands[2])
        val gson = Gson()
        print(gson.toJson(cut.historyForLastNDays(10)))

        val commandsList = (1..10).map { Command(it, "Command $it") }.toList()
        val sortedCommands = cut.sortCommands(commandsList)
        Assert.assertEquals(10, sortedCommands.size)
        Assert.assertEquals(3, sortedCommands[0].number)
        Assert.assertEquals(2, sortedCommands[1].number)
        Assert.assertEquals(1, sortedCommands[2].number)
    }
}