package eu.me2d.cmlmobile.api

import okhttp3.RequestBody
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST

interface ApiRetrofitService {

    @POST("clients")
    fun postPublicKey(@Body request: PublicKeyRequest): Call<PublicKeyResponse>

    @GET("commands")
    fun getCommands(@Header("Authorization") authorization: String): Call<List<Command>>
}