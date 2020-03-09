package eu.me2d.cmlmobile


import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.activityViewModels
import eu.me2d.cmlmobile.databinding.FragmentSetupBinding

/**
 * A simple [Fragment] subclass.
 */
class SetupFragment : Fragment() {

    private val viewModel: CmlViewModel by activityViewModels()
    private lateinit var binding: FragmentSetupBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        binding = FragmentSetupBinding.inflate(inflater)
        binding.viewModel = viewModel
        binding.lifecycleOwner = this
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        binding.sendButton.setOnClickListener {viewModel.sendRegisterClientRequest()}
    }




}
