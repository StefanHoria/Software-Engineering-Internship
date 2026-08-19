package aplicatie.isbn

enum class ScanMode { ISBN, TITLE }

data class BookHit(
    val isbn: String? = null,
    val title: String? = null,
    val authors: String? = null,
    val googleUrl: String? = null
)
