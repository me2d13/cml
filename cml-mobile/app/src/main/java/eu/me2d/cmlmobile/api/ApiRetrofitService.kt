package eu.me2d.cmlmobile.api

import okhttp3.RequestBody
import retrofit2.Call
import retrofit2.http.*

interface ApiRetrofitService {

    @POST("clients")
    fun postPublicKey(@Body request: PublicKeyRequest): Call<PublicKeyResponse>

    @GET("commands")
    fun getCommands(@Header("Authorization") authorization: String): Call<List<Command>>

    @POST("commands/{num}")
    fun executeCommand(@Header("Authorization") authorization: String, @Path("num") number: Number): Call<Void>
}