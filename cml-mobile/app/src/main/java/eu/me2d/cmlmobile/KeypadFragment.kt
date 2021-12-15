package eu.me2d.cmlmobile

import android.os.Bundle
import android.text.method.ScrollingMovementMethod
import android.view.*
import androidx.fragment.app.Fragment
import android.widget.Button
import android.widget.Toast
import androidx.core.content.ContextCompat
import androidx.databinding.BindingAdapter
import androidx.fragment.app.activityViewModels
import androidx.lifecycle.Observer
import androidx.navigation.findNavController
import androidx.navigation.ui.NavigationUI
import com.google.android.material.floatingactionbutton.FloatingActionButton
import eu.me2d.cmlmobile.databinding.FragmentKeypadBinding


class KeypadFragment : Fragment() {
    private val vm: CmlViewModel by activityViewModels()
    private lateinit var binding: FragmentKeypadBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        setHasOptionsMenu(true)
        binding = FragmentKeypadBinding.inflate(inflater)
        // Inflate the layout for this fragment
        binding.viewModel = vm
        binding.lifecycleOwner = this
        vm.toastCode.observe(viewLifecycleOwner, {
            if (it == 403) {
                Toast.makeText(this.context, R.string.not_yet_approved, Toast.LENGTH_SHORT).show()
            } else if ( it != 200) {
                Toast.makeText(this.context, it.toString(), Toast.LENGTH_SHORT).show()
            }
        })
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        binding.apply {
            input.text = ""
            b1.setOnClickListener { v -> onNumberClick(v) }
            b2.setOnClickListener { v -> onNumberClick(v) }
            b3.setOnClickListener { v -> onNumberClick(v) }
            b4.setOnClickListener { v -> onNumberClick(v) }
            b5.setOnClickListener { v -> onNumberClick(v) }
            b6.setOnClickListener { v -> onNumberClick(v) }
            b9.setOnClickListener { v -> onNumberClick(v) }
            b7.setOnClickListener { v -> onNumberClick(v) }
            b8.setOnClickListener { v -> onNumberClick(v) }
            b0.setOnClickListener { v -> onNumberClick(v) }
            bc.setOnClickListener { input.text = "" }
            be.setOnClickListener { onEnterPressed() }
            floatingActionButton.setOnClickListener { vm.fetchCommands() }
            commandsTextView.movementMethod = ScrollingMovementMethod();
        }
    }

    private fun onNumberClick(v: View) {
        val button: Button = v as Button
        binding.input.text = String.format("%s%s", binding.input.text, button.text)
    }


    private fun onEnterPressed() {
        vm.executeCommand(Integer.parseInt(binding.input.text.toString()))
        binding.input.text = ""
    }

    override fun onCreateOptionsMenu(menu: Menu, inflater: MenuInflater) {
        super.onCreateOptionsMenu(menu, inflater)
        inflater.inflate(R.menu.menu_main, menu)
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return NavigationUI.onNavDestinationSelected(item,
            requireView().findNavController())
                || super.onOptionsItemSelected(item)
    }

}

@BindingAdapter("android:clickable")
fun setClickable(view: View, clickable: Boolean) {
    val fab: FloatingActionButton = view as FloatingActionButton
    fab.isClickable = clickable
    fab.backgroundTintList = ContextCompat.getColorStateList(fab.context, if (clickable) R.color.colorAccent else R.color.colorDark)
}
