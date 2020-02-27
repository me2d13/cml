package eu.me2d.cmlmobile.api

import androidx.lifecycle.MutableLiveData
import io.jsonwebtoken.Jwts
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import timber.log.Timber
import java.security.PrivateKey
import java.security.SecureRandom
import java.security.cert.X509Certificate
import java.util.*
import javax.net.ssl.*


//TODO: convert to Dagger singleton
class ApiService(baseUrl: String, private val privateKey: PrivateKey) {
    private val retrofitService = Retrofit.Builder()
        .baseUrl(baseUrl)
        .addConverterFactory(GsonConverterFactory.create())
        .client(unSafeOkHttpClient().addInterceptor(HttpLoggingInterceptor()).build())
        .build()
        .create(ApiRetrofitService::class.java)

    init {
        Timber.d("Created retrofit with base url %s", baseUrl)
    }

    fun register(certificate: String, note: String?, result: MutableLiveData<String>) {
        val call = retrofitService.postPublicKey(PublicKeyRequest(certificate, note))
        call.enqueue(object : Callback<PublicKeyResponse> {
            override fun onFailure(call: Call<PublicKeyResponse>, t: Throwable) {
                result.value = t.localizedMessage
                Timber.e(t, "Api error")
            }

            override fun onResponse(
                call: Call<PublicKeyResponse>,
                response: Response<PublicKeyResponse>
            ) {
                if (response.isSuccessful) {
                    result.value = "OK ${response.body()?.message}"
                } else {
                    result.value = "${response.code()} ${response.message()}"
                }
            }
        })
    }

    private fun unSafeOkHttpClient() :OkHttpClient.Builder {
        val okHttpClient = OkHttpClient.Builder()
        try {
            // Create a trust manager that does not validate certificate chains
            val trustAllCerts:  Array<TrustManager> = arrayOf(object : X509TrustManager {
                override fun checkClientTrusted(chain: Array<out X509Certificate>?, authType: String?){}
                override fun checkServerTrusted(chain: Array<out X509Certificate>?, authType: String?) {}
                override fun getAcceptedIssuers(): Array<X509Certificate>  = arrayOf()
            })

            // Install the all-trusting trust manager
            val  sslContext = SSLContext.getInstance("SSL")
            sslContext.init(null, trustAllCerts, SecureRandom())

            // Create an ssl socket factory with our all-trusting manager
            val sslSocketFactory = sslContext.socketFactory
            if (trustAllCerts.isNotEmpty() &&  trustAllCerts.first() is X509TrustManager) {
                okHttpClient.sslSocketFactory(sslSocketFactory, trustAllCerts.first() as X509TrustManager)
                okHttpClient.hostnameVerifier(HostnameVerifier() { _, _ -> true})
            }

            return okHttpClient
        } catch (e: Exception) {
            return okHttpClient
        }
    }

    fun fetchCommands(commands: MutableLiveData<List<Command>>) {
        val jws = Jwts.builder()
            .setSubject("Commands")
            .setId(Date().time.toString())
            .signWith(privateKey)
            .compact()
        val call = retrofitService.getCommands("Bearer $jws")
        call.enqueue(object : Callback<List<Command>> {
            override fun onFailure(call: Call<List<Command>>, t: Throwable) {
                commands.value = Collections.emptyList()
                Timber.e(t, "Api error")
            }

            override fun onResponse(call: Call<List<Command>>, response: Response<List<Command>>) {
                if (response.isSuccessful) {
                    Timber.d("Fetched %d commands", response.body()?.size)
                    commands.value = response.body()
                } else {
                    Timber.e("${response.code()} ${response.message()}")
                    commands.value = Collections.emptyList()
                }
            }
        })
    }

    fun executeCommand(number: Number) {
        val jws = Jwts.builder()
            .setSubject("Command")
            .setId(Date().time.toString())
            .signWith(privateKey)
            .compact()
        val call = retrofitService.executeCommand("Bearer $jws", number)
        call.enqueue(object : Callback<Void> {
            override fun onFailure(call: Call<Void>, t: Throwable) {
                Timber.e(t, "Api error")
            }

            override fun onResponse(call: Call<Void>, response: Response<Void>) {
                if (response.isSuccessful) {
                    Timber.d("Executed command %d", number.toInt())
                } else {
                    Timber.e("${response.code()} ${response.message()}")
                }
            }
        })
    }
}