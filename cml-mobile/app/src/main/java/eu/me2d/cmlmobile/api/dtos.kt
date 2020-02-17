package eu.me2d.cmlmobile.api

import com.google.gson.annotations.SerializedName

data class PublicKeyRequest(
    val key: String,
    val message: String?
)

data class PublicKeyResponse(
    @SerializedName("message")
    val message: String
)

data class Command(
    val number: Int,
    val description: String
)