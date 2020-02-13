package eu.me2d.cmlmobile

import android.os.Bundle
import android.view.*
import androidx.fragment.app.Fragment
import android.widget.Button
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.findNavController
import androidx.navigation.ui.NavigationUI
import eu.me2d.cmlmobile.databinding.FragmentKeypadBinding


class KeypadFragment : Fragment() {
    private lateinit var viewModel: CmlViewModel
    private lateinit var binding: FragmentKeypadBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        setHasOptionsMenu(true)
        val viewModelFactory = CmlViewModelFactory(activity!!.application)
        viewModel = ViewModelProvider(this, viewModelFactory).get(CmlViewModel::class.java)
        binding = FragmentKeypadBinding.inflate(inflater)
        // Inflate the layout for this fragment
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        binding.apply {
            input.text = ""
            b1.setOnClickListener { v -> onClick(v) }
            b2.setOnClickListener { v -> onClick(v) }
            b3.setOnClickListener { v -> onClick(v) }
            b4.setOnClickListener { v -> onClick(v) }
            b5.setOnClickListener { v -> onClick(v) }
            b6.setOnClickListener { v -> onClick(v) }
            b9.setOnClickListener { v -> onClick(v) }
            b7.setOnClickListener { v -> onClick(v) }
            b8.setOnClickListener { v -> onClick(v) }
            b0.setOnClickListener { v -> onClick(v) }
            bc.setOnClickListener { input.text = "" }
            be.setOnClickListener { onEnterPressed() }
        }
    }

    private fun onClick(v: View) {
        val button: Button = v as Button
        binding.input.text = String.format("%s%s", binding.input.text, button.text)
    }


    fun onEnterPressed() {

    }

    override fun onCreateOptionsMenu(menu: Menu, inflater: MenuInflater) {
        super.onCreateOptionsMenu(menu, inflater)
        inflater.inflate(R.menu.menu_main, menu)
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return NavigationUI.onNavDestinationSelected(item,
            view!!.findNavController())
                || super.onOptionsItemSelected(item)
    }
}
