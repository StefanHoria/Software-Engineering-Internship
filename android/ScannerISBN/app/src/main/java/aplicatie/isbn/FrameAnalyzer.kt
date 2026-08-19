package aplicatie.isbn


import android.graphics.Bitmap
import androidx.annotation.OptIn
import androidx.camera.core.ExperimentalGetImage
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import com.google.android.gms.tasks.Tasks
import com.google.mlkit.vision.barcode.common.Barcode
import com.google.mlkit.vision.barcode.BarcodeScannerOptions
import com.google.mlkit.vision.barcode.BarcodeScanning
import com.google.mlkit.vision.common.InputImage
import com.google.mlkit.vision.text.TextRecognition
import com.google.mlkit.vision.text.latin.TextRecognizerOptions

class FrameAnalyzer(
    private val modeProvider: () -> ScanMode,
    private val onResult: (String?, String?) -> Unit // (isbn, title)
) : ImageAnalysis.Analyzer {

    private val barcodeScanner = BarcodeScanning.getClient(
        BarcodeScannerOptions.Builder()
            .setBarcodeFormats(Barcode.FORMAT_EAN_13, Barcode.FORMAT_EAN_8)
            .build()
    )
    private val textRecognizer = TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS)

    private var lastTs = 0L

    @OptIn(ExperimentalGetImage::class)
    override fun analyze(imageProxy: ImageProxy) {
        val media = imageProxy.image ?: run { imageProxy.close(); return }
        val img = InputImage.fromMediaImage(media, imageProxy.imageInfo.rotationDegrees)

        val now = System.currentTimeMillis()
        val throttle = now - lastTs < 1500
        val mode = modeProvider()

        when (mode) {
            ScanMode.ISBN -> {
                barcodeScanner.process(img)
                    .addOnSuccessListener { codes ->
                        val raw = codes.firstOrNull()?.rawValue
                        val isbn = raw?.trim()?.replace("-", "")
                        if (!throttle && isbn != null && (isbn.length == 13 || isbn.length == 8)) {
                            lastTs = System.currentTimeMillis()
                            onResult(isbn, null)
                        }
                    }
                    .addOnCompleteListener { imageProxy.close() }
            }
            ScanMode.TITLE -> {
                // pentru OCR pe cotor: alegem ROI central și încercăm rotiri
                val bmp = imageProxy.toBitmap()  // extensie utilă, vezi mai jos
                val rois = makeSpineRois(bmp)    // benzi verticale
                var best: String? = null
                for (roi in rois) {
                    // 0°, 90°, 270° – cresc șansele la cotoare verticale
                    val candidates = listOf(roi, roi.rotate90(), roi.rotate270())
                    for (c in candidates) {
                        val input = InputImage.fromBitmap(c, 0)
                        val txt = Tasks.await(textRecognizer.process(input))?.text ?: ""
                        val pick = pickLikelyTitle(txt)
                        if (!pick.isNullOrBlank() && pick.length > (best?.length ?: 0)) {
                            best = pick
                        }
                    }
                }
                if (!throttle && !best.isNullOrBlank()) {
                    lastTs = System.currentTimeMillis()
                    onResult(null, best!!.trim())
                }
                imageProxy.close()
            }
        }
    }

    // Heuristică pt. titlu
    private fun pickLikelyTitle(full: String): String? {
        val lines = full.split('\n').map { it.trim() }.filter { it.length >= 3 }
        val scored = lines.map { line ->
            val digits = line.count { it.isDigit() }
            val words3 = line.split(" ").count { it.length >= 3 }
            val penalty = if (digits > line.length * 0.5) 2 else 0
            val score = words3 - penalty + if (line.any { it.isUpperCase() }) 1 else 0
            line to score
        }.sortedByDescending { it.second }
        return scored.firstOrNull()?.first
    }

    // ROI: 2–3 benzi verticale în zona centrală
    private fun makeSpineRois(bmp: Bitmap): List<Bitmap> {
        val w = bmp.width; val h = bmp.height
        val bands = ArrayList<Bitmap>()
        val bandW = (w * 0.28f).toInt()
        val xs = listOf((w*0.36f).toInt(), (w*0.18f).toInt(), (w*0.54f).toInt()).map { it.coerceIn(0, w-bandW) }
        for (x in xs) {
            bands += Bitmap.createBitmap(bmp, x, 0, bandW, h)
        }
        return bands
    }
}
