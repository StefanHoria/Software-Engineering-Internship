package aplicatie.isbn

import retrofit2.http.GET
import retrofit2.http.Query

interface BooksApi {
    @GET("volumes")
    suspend fun byIsbn(@Query("q") q: String): BooksResponse

    @GET("volumes")
    suspend fun byTitle(@Query("q") q: String, @Query("maxResults") max: Int = 5): BooksResponse
}

data class BooksResponse(val items: List<BookItem>?)
data class BookItem(val id: String?, val volumeInfo: VolumeInfo?)
data class VolumeInfo(
    val title: String?, val authors: List<String>?, val publisher: String?,
    val publishedDate: String?, val description: String?, val imageLinks: ImageLinks?
)
data class ImageLinks(val thumbnail: String?)
