package com.example.restnestadmin.api

import com.example.restnestadmin.Order
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Body
import retrofit2.http.Path

data class OrdersResponse(val success: Boolean, val orders: List<Order>)
data class BulkOrder(
    val id: String,
    val first_name: String,
    val last_name: String,
    val email: String,
    val phone: String,
    val address: String,
    val city: String,
    val state: String,
    val pincode: String,
    val status: String,
    val created_at: String
)
data class BulkOrdersResponse(val success: Boolean, val bulkOrders: List<BulkOrder>)

interface RestNestApi {
    @GET("api/orders")
    suspend fun getOrders(): OrdersResponse

    @GET("api/bulk-orders")
    suspend fun getBulkOrders(): BulkOrdersResponse
}

object RetrofitClient {
    private const val BASE_URL = "https://restienestie.onrender.com/"
    
    val instance: RestNestApi by lazy {
        val retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
        retrofit.create(RestNestApi::class.java)
    }
}