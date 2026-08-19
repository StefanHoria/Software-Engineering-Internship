package com.example.visiondemo

import android.content.Context
import android.graphics.Bitmap
import android.util.Log

class Hands(ctx: Context, private val historySize: Int = 5) {

    // Folosim FQN ca să evităm erori de import
    private val landmarker: com.google.mediapipe.tasks.vision.handlandmarker.HandLandmarker
    private var ts = 0L // timestamp ms pentru RunningMode.VIDEO

    // ------------ calibrare ușoară ------------
    private val TH_OPEN = 55.0   // prag pentru index/middle/ring/pinky (unghi mic = deget întins)
    private val TH_THUMB = 50.0  // prag pentru degetul mare (MCP unghi mic = întins)
    private val DET_CONF = 0.50f // înalță dacă vrei mai puține false pozitive (0.35..0.70)
    private val TRK_CONF = 0.50f
    // ------------------------------------------

    init {
        val base = com.google.mediapipe.tasks.core.BaseOptions.builder()
            .setModelAssetPath("hand_landmarker.task")
            .build()

        val opts = com.google.mediapipe.tasks.vision.handlandmarker.HandLandmarkerOptions
            .builder()
            .setBaseOptions(base)
            .setRunningMode(com.google.mediapipe.tasks.vision.core.RunningMode.VIDEO)
            .setNumHands(2)
            .setMinHandDetectionConfidence(DET_CONF)
            .setMinTrackingConfidence(TRK_CONF)
            .build()

        landmarker = com.google.mediapipe.tasks.vision.handlandmarker.HandLandmarker
            .createFromOptions(ctx, opts)

        Log.d("Hands", "HandLandmarker OK (det=$DET_CONF trk=$TRK_CONF)")
    }

    data class FingerState(
        val thumb: Boolean,
        val index: Boolean,
        val middle: Boolean,
        val ring: Boolean,
        val pinky: Boolean,
        val count: Int,
        val handedness: String, // "Left"/"Right"
        val score: Float
    ) {
        val label: String get() = "$handedness:$count"
    }

    // ——— smoothing pe fiecare deget (vot majoritar) ———
    private val histThumb  = ArrayDeque<Boolean>()
    private val histIndex  = ArrayDeque<Boolean>()
    private val histMiddle = ArrayDeque<Boolean>()
    private val histRing   = ArrayDeque<Boolean>()
    private val histPinky  = ArrayDeque<Boolean>()

    private fun smooth(q: ArrayDeque<Boolean>, v: Boolean, N: Int = historySize): Boolean {
        q.addLast(v)
        if (q.size > N) q.removeFirst()
        val trues = q.count { it }
        return trues >= (q.size + 1) / 2
    }
    // ————————————————————————————————————————

    fun infer(bmp: Bitmap): List<FingerState> {
        val mpImg = com.google.mediapipe.framework.image.BitmapImageBuilder(bmp).build()
        ts += 33 // ~30 FPS; poți folosi și SystemClock.uptimeMillis()
        val res = landmarker.detectForVideo(mpImg, ts)

        val out = mutableListOf<FingerState>()
        val hands = res.landmarks()
        val handed = res.handednesses()

        // log util: câte mâini vede
        // Log.d("Hands", "Detected hands=${hands.size}")

        for (i in hands.indices) {
            val pts = hands[i]
            val handLabel = handed[i][0].categoryName()
            val score = handed[i][0].score()

            // unghi ∠ABC (grade) între BA și BC, în 3D (x,y,z normalizate)
            fun angle(a: Int, b: Int, c: Int): Double {
                val ax = pts[a].x(); val ay = pts[a].y(); val az = pts[a].z()
                val bx = pts[b].x(); val by = pts[b].y(); val bz = pts[b].z()
                val cx = pts[c].x(); val cy = pts[c].y(); val cz = pts[c].z()
                val v1x = ax - bx; val v1y = ay - by; val v1z = az - bz
                val v2x = cx - bx; val v2y = cy - by; val v2z = cz - bz
                val dot = v1x*v2x + v1y*v2y + v1z*v2z
                val n1 = Math.sqrt((v1x*v1x + v1y*v1y + v1z*v1z).toDouble())
                val n2 = Math.sqrt((v2x*v2x + v2y*v2y + v2z*v2z).toDouble())
                val cos = (dot / (n1 * n2)).coerceIn(-1.0, 1.0)
                return Math.toDegrees(Math.acos(cos))
            }

            // Index/Middle/Ring/Pinky: unghi mic la PIP (MCP-PIP-TIP) => deget întins
            fun isFingerUp(mcp: Int, pip: Int, tip: Int) = angle(mcp, pip, tip) < TH_OPEN
            val indexUp  = isFingerUp(5, 6, 8)
            val middleUp = isFingerUp(9, 10, 12)
            val ringUp   = isFingerUp(13, 14, 16)
            val pinkyUp  = isFingerUp(17, 18, 20)

            // Thumb: unghi mic la MCP (CMC-MCP-TIP => 1-2-4) => întins
            val thumbUp = angle(1, 2, 4) < TH_THUMB

            // smoothing per deget
            val sThumb  = smooth(histThumb,  thumbUp)
            val sIndex  = smooth(histIndex,  indexUp)
            val sMiddle = smooth(histMiddle, middleUp)
            val sRing   = smooth(histRing,   ringUp)
            val sPinky  = smooth(histPinky,  pinkyUp)

            var cnt = 0
            if (sThumb)  cnt++
            if (sIndex)  cnt++
            if (sMiddle) cnt++
            if (sRing)   cnt++
            if (sPinky)  cnt++

            out += FingerState(
                sThumb, sIndex, sMiddle, sRing, sPinky,
                cnt, handLabel, score
            )
        }
        return out
    }
}
