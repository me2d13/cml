package eu.me2d.cmlmobile


import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.lifecycle.ViewModelProvider
import eu.me2d.cmlmobile.databinding.FragmentSetupBinding

/**
 * A simple [Fragment] subclass.
 */
class SetupFragment : Fragment() {

    private lateinit var viewModel: CmlViewModel
    private lateinit var binding: FragmentSetupBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val viewModelFactory = CmlViewModelFactory(activity!!.application)
        viewModel = ViewModelProvider(this, viewModelFactory).get(CmlViewModel::class.java)
        binding = FragmentSetupBinding.inflate(inflater)
        binding.viewModel = viewModel
        binding.lifecycleOwner = this
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        binding.sendButton.setOnClickListener {viewModel.onSendRequest()}
    }




}
