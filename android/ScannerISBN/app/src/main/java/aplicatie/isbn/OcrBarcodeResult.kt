package aplicatie.isbn

data class OcrBarcodeResult(
    val isbn13: String? = null,
    val titleCandidate: String? = null
)