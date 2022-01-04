package eu.me2d.cmlmobile.list

import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import eu.me2d.cmlmobile.CmlViewModel
import eu.me2d.cmlmobile.api.Command
import eu.me2d.cmlmobile.databinding.FragmentItemBinding
import timber.log.Timber

class MyCommandRecyclerViewAdapter(
    private val vm: CmlViewModel
) : RecyclerView.Adapter<MyCommandRecyclerViewAdapter.ViewHolder>() {

    private val values = vm.historyService.sortCommands(vm.commands.value ?: emptyList())

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {

        return ViewHolder(
            FragmentItemBinding.inflate(
                LayoutInflater.from(parent.context),
                parent,
                false
            )
        )

    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = values[position]
        holder.idView.text = item.number.toString()
        holder.contentView.text = item.description
        holder.wrapper.setOnClickListener {
            Timber.d("Click on number %d", item.number)
            vm.executeCommand(item.number)
        }
    }

    override fun getItemCount(): Int = values.size

    inner class ViewHolder(binding: FragmentItemBinding) : RecyclerView.ViewHolder(binding.root) {
        val idView: TextView = binding.itemNumber
        val contentView: TextView = binding.content
        val wrapper = binding.itemWrap

        override fun toString(): String {
            return super.toString() + " '" + contentView.text + "'"
        }
    }

}