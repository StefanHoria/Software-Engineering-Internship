package com.example.visiondemo

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.*
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.util.Size
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.annotation.OptIn
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.*
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.content.ContextCompat
import com.google.mlkit.vision.common.InputImage
import com.google.mlkit.vision.face.FaceDetection
import com.google.mlkit.vision.face.FaceDetector
import com.google.mlkit.vision.face.FaceDetectorOptions
import java.io.ByteArrayOutputStream
import java.util.Locale
import java.util.concurrent.Executors

class MainActivity : AppCompatActivity() {

    private lateinit var previewView: PreviewView
    private lateinit var statusText: TextView
    private lateinit var btnTts: Button
    private lateinit var btnTorch: Button

    private var tts: TextToSpeech? = null
    private var ttsOn = true
    private var torchOn = false

    private var eag: Eag? = null
    private var hands: Hands? = null

    private var camera: androidx.camera.core.Camera? = null
    private lateinit var provider: ProcessCameraProvider
    private val exec = Executors.newSingleThreadExecutor()

    private val askCamPerm = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted -> if (granted) startCamera() else toast("Camera denied") }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        previewView = findViewById(R.id.previewView)
        statusText = findViewById(R.id.statusText)
        btnTts = findViewById(R.id.btnToggleTts)
        btnTorch = findViewById(R.id.btnTorch)

        // modele
        eag = Eag.fromAssets(this)
        hands = Hands(this)

        // TTS
        tts = TextToSpeech(this) { s ->
            if (s == TextToSpeech.SUCCESS) {
                val ok = tts?.setLanguage(Locale("ro", "RO"))
                if (ok == TextToSpeech.LANG_MISSING_DATA || ok == TextToSpeech.LANG_NOT_SUPPORTED) {
                    tts?.language = Locale.US
                }
            }
        }

        btnTts.setOnClickListener { ttsOn = !ttsOn; status("TTS: ${if (ttsOn) "ON" else "OFF"}") }
        btnTorch.setOnClickListener { toggleTorch() }

        if (hasCamPermission()) startCamera() else askCamPerm.launch(Manifest.permission.CAMERA)
    }

    private fun hasCamPermission() =
        ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED

    private fun startCamera() {
        val future = ProcessCameraProvider.getInstance(this)
        future.addListener({
            provider = future.get()

            val preview = Preview.Builder().build().also {
                it.setSurfaceProvider(previewView.surfaceProvider)
            }

            val analysis = ImageAnalysis.Builder()
                .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                .setTargetResolution(Size(1280, 720))
                .setOutputImageFormat(ImageAnalysis.OUTPUT_IMAGE_FORMAT_YUV_420_888)
                .build()
                .also { it.setAnalyzer(exec) { analyzeFrame(it) } }

            provider.unbindAll()
            camera = provider.bindToLifecycle(
                this, CameraSelector.DEFAULT_FRONT_CAMERA, preview, analysis
            )

            status("Pornit. Zâmbește și arată degete ✋")
        }, ContextCompat.getMainExecutor(this))
    }

    // ML Kit FaceDetector pentru ROI rapid
    private val faceDetector: FaceDetector by lazy {
        val opts = FaceDetectorOptions.Builder()
            .setPerformanceMode(FaceDetectorOptions.PERFORMANCE_MODE_FAST)
            .enableTracking()
            .build()
        FaceDetection.getClient(opts)
    }

    private var lastTtsTs = 0L

    @OptIn(ExperimentalGetImage::class)
    private fun analyzeFrame(proxy: ImageProxy) {
        val media = proxy.image ?: run { proxy.close(); return }
        val rotation = proxy.imageInfo.rotationDegrees

        fun Bitmap.rotate(degrees: Int): Bitmap {
            val matrix = Matrix().apply { postRotate(degrees.toFloat()) }
            return Bitmap.createBitmap(this, 0, 0, width, height, matrix, true)
        }

        // 1) Bitmap upright pentru Hands + crop față
        val bmp = proxy.toBitmap()
        val upright = bmp.rotate(rotation)

        // 2) ML Kit pe frame-ul NV21 (via InputImage) cu rotația corectă
        val image = InputImage.fromMediaImage(media, rotation)

        faceDetector.process(image)
            .addOnSuccessListener { faces ->
                // HANDS (pe imaginea rotită!)
                val handRes = hands?.infer(upright).orEmpty()
                val handsLabel = handRes.joinToString(" | ") { it.label }

                // FACE → EAG (emo/gen/age)
                var emo = ""; var gen = ""; var age = -1
                val face = faces.maxByOrNull { it.boundingBox.width() * it.boundingBox.height() }
                if (face != null) {
                    val r = face.boundingBox
                    val roi = upright.cropSafe(r)
                    val (e, g, a) = eag!!.predictAll(roi)
                    emo = e; gen = g; age = a
                }

                // HUD + TTS
                val txt = buildString {
                    if (emo.isNotEmpty()) append("$emo | $age | $gen")
                    if (handsLabel.isNotEmpty()) append(if (isNotEmpty()) " • " else "").append(handsLabel)
                }
                status(if (txt.isEmpty()) "Nimic detectat" else txt)

                val now = System.currentTimeMillis()
                if (ttsOn && txt.isNotEmpty() && now - lastTtsTs > 1500) {
                    tts?.speak(txt, TextToSpeech.QUEUE_FLUSH, null, "tts")
                    lastTtsTs = now
                }
            }
            .addOnFailureListener { e -> e.printStackTrace() }
            .addOnCompleteListener { proxy.close() }
    }

    private fun toggleTorch() {
        torchOn = !torchOn
        camera?.cameraControl?.enableTorch(torchOn)
        status("Torch: ${if (torchOn) "ON" else "OFF"}")
    }

    private fun status(s: String) = runOnUiThread { statusText.text = s }
    private fun toast(s: String) = runOnUiThread { Toast.makeText(this, s, Toast.LENGTH_SHORT).show() }

    override fun onDestroy() {
        super.onDestroy()
        tts?.shutdown()
        exec.shutdown()
    }
}

