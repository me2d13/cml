package eu.me2d.cmlmobile.car

import android.annotation.SuppressLint
import androidx.car.app.CarContext
import androidx.car.app.Screen
import androidx.car.app.model.Action
import androidx.car.app.model.ItemList
import androidx.car.app.model.ListTemplate
import androidx.car.app.model.Row
import androidx.car.app.model.Template
import androidx.car.app.utils.ThreadUtils
import eu.me2d.cmlmobile.api.Command
import timber.log.Timber
import java.util.function.Consumer

class MainCmlCarScreen(
    carContext: CarContext,
    private val commands: List<Command>,
    private val onCommandClick: Consumer<Int>
) : Screen(carContext) {

    private var loadedCommandNo: Int? = null

    @SuppressLint("RestrictedApi")
    private fun newResetThread(): Thread {
        return Thread {
            Thread.sleep(3000)
            loadedCommandNo = null
            Timber.d("Active command timed out")
            ThreadUtils.runOnMain {
                invalidate()
            }
        }
    }

    override fun onGetTemplate(): Template {
        val listBuilder = ItemList.Builder()
        commands.forEach { listBuilder.addItem(commandToRow(it)) }

        return ListTemplate.Builder()
            .setSingleList(listBuilder.build())
            .setHeaderAction(Action.APP_ICON)
            .setTitle("Command")
            .build()
    }

    private fun commandToRow(command: Command): Row {
        val text = "${command.number} - ${command.description}"
        return Row.Builder()
            .setTitle(text)
            .setBrowsable(loadedCommandNo == command.number)
            .setOnClickListener {
                loadedCommandNo = if (loadedCommandNo == command.number) {
                    onCommandClick.accept(command.number)
                    null
                } else {
                    newResetThread().start()
                    command.number
                }
                invalidate()
            }
            .build()
    }
}