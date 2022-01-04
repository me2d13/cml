package eu.me2d.cmlmobile

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.core.content.res.ResourcesCompat
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.viewpager2.adapter.FragmentStateAdapter
import androidx.viewpager2.widget.ViewPager2
import com.google.android.material.tabs.TabLayout
import com.google.android.material.tabs.TabLayoutMediator
import eu.me2d.cmlmobile.list.CommandsListFragment

class MainFragment : Fragment() {

    private lateinit var viewPager: ViewPager2
    private lateinit var adapter: ScreenSlidePagerAdapter
    private val viewModel: CmlViewModel by viewModels()


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_main, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        adapter = ScreenSlidePagerAdapter(this)
        viewPager = view.findViewById(R.id.pager)
        viewPager.adapter = adapter

        viewPager.currentItem = viewModel.currentTab
        val tabLayout = view.findViewById<TabLayout>(R.id.tabLayout)

        tabLayout.addOnTabSelectedListener(object : TabLayout.OnTabSelectedListener {
            override fun onTabSelected(tab: TabLayout.Tab?) {
                viewModel.currentTab = tab?.position ?: 0
            }

            override fun onTabUnselected(tab: TabLayout.Tab?) {
            }

            override fun onTabReselected(tab: TabLayout.Tab?) {
            }
        })

        TabLayoutMediator(tabLayout, viewPager) { tab, position ->
            tab.text = null
            tab.icon = when (position) {
                0 -> ContextCompat.getDrawable(context!!, R.drawable.ic_keypad)
                1 -> ContextCompat.getDrawable(context!!,R.drawable.ic_list)
                else -> TODO("FAV")
            }
        }.attach()
    }

    private inner class ScreenSlidePagerAdapter(fa: Fragment) : FragmentStateAdapter(fa) {
        override fun getItemCount(): Int = 2

        override fun createFragment(position: Int): Fragment {
            return when (position) {
                0 -> KeypadFragment()
                1 -> CommandsListFragment()
                else -> CommandsListFragment()
            }
        }
    }

}