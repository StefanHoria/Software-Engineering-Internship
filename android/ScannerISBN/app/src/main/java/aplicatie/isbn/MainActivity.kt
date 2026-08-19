package aplicatie.isbn



import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.util.Size
import android.view.MotionEvent
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.Camera
import androidx.camera.core.CameraSelector
import androidx.camera.core.FocusMeteringAction
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.content.ContextCompat
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.Locale
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

private val MainActivity.url: String? // Make it nullable as lastHit can be null
    get() {
        val hit = lastHit ?: return null // Return null if lastHit is null
        return when {
            !hit.isbn.isNullOrBlank() -> "https://www.google.com/search?q=isbn:${hit.isbn}"
            !hit.title.isNullOrBlank() -> "https://www.google.com/search?q=" + Uri.encode(hit.title + " " + (hit.authors ?: ""))
            else -> null
        }
    }

class MainActivity : AppCompatActivity() {

    private lateinit var previewView: PreviewView
    private lateinit var statusText: TextView
    private lateinit var btnIsbn: Button
    private lateinit var btnTitle: Button
    private lateinit var btnTorch: Button
    private lateinit var btnBrowser: Button
    private lateinit var btnShare: Button

    private var mode = ScanMode.ISBN
    public var lastHit: BookHit? = null
    private var torchOn = false

    private var camera: Camera? = null
    private lateinit var cameraProvider: ProcessCameraProvider
    private val camExecutor = Executors.newSingleThreadExecutor()
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        previewView = findViewById(R.id.previewView)
        statusText = findViewById(R.id.statusText)
        btnIsbn = findViewById(R.id.btnIsbn)
        btnTitle = findViewById(R.id.btnTitle)
        btnTorch = findViewById(R.id.btnTorch)
        btnBrowser = findViewById(R.id.btnBrowser)
        btnShare = findViewById(R.id.btnShare)

        btnIsbn.setOnClickListener { mode = ScanMode.ISBN; status("Mod: ISBN") }
        btnTitle.setOnClickListener { mode = ScanMode.TITLE; status("Mod: Titlu") }
        btnTorch.setOnClickListener { toggleTorch() }
        btnBrowser.setOnClickListener { openInBrowser() }
        btnShare.setOnClickListener { shareHit() }

        // tap-to-focus
        previewView.setOnTouchListener { _, ev ->
            if (ev.action == MotionEvent.ACTION_UP && camera != null) {
                val point = previewView.meteringPointFactory.createPoint(ev.x, ev.y)
                val action = FocusMeteringAction.Builder(point, FocusMeteringAction.FLAG_AF)
                    .setAutoCancelDuration(2, TimeUnit.SECONDS).build()
                camera!!.cameraControl.startFocusAndMetering(action)
            }
            true
        }

        if (hasCam()) startCamera() else requestPerm()
    }

    private fun requestPerm() = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { if (it) startCamera() else status("Camera permission denied") }
        .launch(Manifest.permission.CAMERA)

    private fun hasCam() =
        ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED

    private fun startCamera() {
        val providerFuture = ProcessCameraProvider.getInstance(this)
        providerFuture.addListener({
            cameraProvider = providerFuture.get()

            val preview = Preview.Builder().build().also {
                it.setSurfaceProvider(previewView.surfaceProvider)
            }

            val analysis = ImageAnalysis.Builder()
                .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                .setTargetResolution(Size(1280, 720)) // puțin mai mare ajută barcode
                .setOutputImageFormat(ImageAnalysis.OUTPUT_IMAGE_FORMAT_YUV_420_888)
                .build().also {
                    it.setAnalyzer(camExecutor, FrameAnalyzer({ mode }) { isbn, title ->
                        handleResult(isbn, title)
                    })
                }

            cameraProvider.unbindAll()
            camera = cameraProvider.bindToLifecycle(
                this, CameraSelector.DEFAULT_BACK_CAMERA, preview, analysis
            )
            status("Mod: ${mode.name} | Torch: ${if (torchOn) "ON" else "OFF"}")
        }, ContextCompat.getMainExecutor(this))
    }

    private fun handleResult(isbn: String?, title: String?) {
        when {
            isbn != null -> {
                status("ISBN: $isbn • caut online…")
                scope.launch {
                    val v = searchByIsbn(isbn)
                    withContext(Dispatchers.Main) {
                        lastHit = v
                        status("ISBN: ${v?.title ?: isbn} • ${v?.authors ?: ""}")
                    }
                }
            }
            !title.isNullOrBlank() -> {
                status("Titlu: $title • caut online…")
                scope.launch {
                    val v = searchByTitle(title)
                    withContext(Dispatchers.Main) {
                        lastHit = v ?: BookHit(title = title)
                        status("Titlu: ${lastHit?.title ?: title} • ${lastHit?.authors ?: ""}")
                    }
                }
            }
        }
    }

    // --- căutare online (Google Books) ---
    private suspend fun searchByIsbn(isbn: String): BookHit? = try {
        val r = BooksClient.api.byIsbn("isbn:$isbn")
        val v = r.items?.firstOrNull()?.volumeInfo
        v?.let {
            BookHit(
                isbn = isbn,
                title = it.title ?: "N/A",
                authors = it.authors?.joinToString(),
                googleUrl = "https://www.google.com/search?q=isbn:$isbn"
            )
        }
    } catch (_: Exception) { null }

    private suspend fun searchByTitle(title: String): BookHit? = try {
        val r = BooksClient.api.byTitle(title)
        val v = r.items?.firstOrNull()?.volumeInfo
        v?.let {
            BookHit(
                title = it.title ?: title,
                authors = it.authors?.joinToString(),
                googleUrl = "https://www.google.com/search?q=" + Uri.encode("${it.title} ${it.authors?.joinToString() ?: ""}")
            )
        }
    } catch (_: Exception) { null }

    // --- Torch ---
    private fun toggleTorch() {
        torchOn = !torchOn
        camera?.cameraControl?.enableTorch(torchOn)
        status("Torch: ${if (torchOn) "ON" else "OFF"} • Mod: ${mode.name}")
    }

    // --- Browser ---
    private fun openInBrowser() {
        val hit = lastHit ?: run { toast("Nimic de deschis"); return }
        val url = when {
            !hit.isbn.isNullOrBlank() -> "https://www.google.com/search?q=isbn:${hit.isbn}"
            !hit.title.isNullOrBlank() -> "https://www.google.com/search?q=" + Uri.encode(hit.title + " " + (hit.authors ?: ""))
            else -> null
        } ?: return
        startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
    }

    // --- Share ---
    private fun shareHit() {
        val hit = lastHit ?: run { toast("Nimic de share-uit"); return }
        val currentBookUrl = this.url // Access the extension property
        val txt = buildString {
            hit.title?.let { append(it) }
            hit.authors?.let { append(" — $it") }
            hit.isbn?.let { append("\nISBN: $it") }
            currentBookUrl?.let { append("\n$it") } // Use the fetched URL
        }
        val i = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, txt)
        }
        startActivity(Intent.createChooser(i, "Trimite cartea"))
    }
    private fun status(s: String) { runOnUiThread { statusText.text = s } }
    private fun toast(s: String) = runOnUiThread { Toast.makeText(this, s, Toast.LENGTH_SHORT).show() }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
        camExecutor.shutdown()
    }
}

