package com.example.visiondemo

import android.content.Context
import android.graphics.*
import android.util.Log
import android.util.Half
import com.google.android.datatransport.BuildConfig
//import org.tensorflow.lite.DataType
import org.tensorflow.lite.Interpreter
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.nio.channels.FileChannel
import kotlin.math.min
import org.tensorflow.lite.DataType



class Eag private constructor(
    private val emo: Interpreter,
    private val gen: Interpreter,
    private val age: Interpreter
) {
    companion object {
        private fun loadInterp(ctx: Context, assetName: String): Interpreter {
            val afd = ctx.assets.openFd(assetName)
            val mapped = afd.createInputStream().channel.map(
                FileChannel.MapMode.READ_ONLY, afd.startOffset, afd.length
            )
            return Interpreter(mapped, Interpreter.Options().apply { setNumThreads(2) })
        }
        fun fromAssets(ctx: Context) = Eag(
            loadInterp(ctx, "emotion_deepface.tflite"),
            loadInterp(ctx, "gender_deepface.tflite"),
            loadInterp(ctx, "age_deepface.tflite")
        )
    }

    private val TAG = "EAG"
    private val EMO = arrayOf("angry","disgust","fear","happy","sad","surprise","neutral")

    private fun scaleBitmap(src: Bitmap, w: Int, h: Int) =
        Bitmap.createScaledBitmap(src, w, h, true)

    private fun toGray(src: Bitmap): Bitmap {
        val out = Bitmap.createBitmap(src.width, src.height, Bitmap.Config.ARGB_8888)
        val c = Canvas(out)
        val p = Paint().apply { colorFilter = ColorMatrixColorFilter(ColorMatrix().apply { setSaturation(0f) }) }
        c.drawBitmap(src, 0f, 0f, p)
        return out
    }

    private data class InSpec(val h:Int, val w:Int, val c:Int, val dt: DataType)
    private fun inputSpec(interp: Interpreter): InSpec {
        val t = interp.getInputTensor(0)
        val s = t.shape() // [1,H,W,C]
        return InSpec(h = s[1], w = s[2], c = s[3], dt = t.dataType())
    }

    /**
     * Construiește input-ul în formatul cerut de TFLite:
     *  - FLOAT32  -> Array(1){H{W{FloatArray(C)}}}
     *  - FLOAT16  -> ByteBuffer direct (H*W*C*2 bytes) cu half-floats
     *  - UINT8    -> ByteBuffer direct (H*W*C bytes)
     */
    private fun makeInput(faceSrc: Bitmap, spec: InSpec): Any {
        val resized = if (spec.c == 1) toGray(scaleBitmap(faceSrc, spec.w, spec.h))
        else scaleBitmap(faceSrc, spec.w, spec.h)

        return when (spec.dt) {
            DataType.FLOAT32 -> {
                val inp = Array(1) { Array(spec.h) { Array(spec.w) { FloatArray(spec.c) } } }
                for (i in 0 until spec.h) for (j in 0 until spec.w) {
                    val px = resized.getPixel(j,i)
                    if (spec.c == 1) {
                        inp[0][i][j][0] = (px and 0xFF) / 255f
                    } else {
                        val r = ((px shr 16) and 0xFF) / 255f
                        val g = ((px shr  8) and 0xFF) / 255f
                        val b = ( px         and 0xFF) / 255f
                        inp[0][i][j][0] = r; inp[0][i][j][1] = g; inp[0][i][j][2] = b
                    }
                }
                inp
            }
            DataType.UINT8 -> {
                val bb = java.nio.ByteBuffer
                    .allocateDirect(spec.h * spec.w * spec.c)
                    .order(java.nio.ByteOrder.nativeOrder())
                for (i in 0 until spec.h) for (j in 0 until spec.w) {
                    val px = resized.getPixel(j,i)
                    if (spec.c == 1) {
                        bb.put((px and 0xFF).toByte())
                    } else {
                        bb.put(((px shr 16) and 0xFF).toByte())
                        bb.put(((px shr  8) and 0xFF).toByte())
                        bb.put(( px         and 0xFF).toByte())
                    }
                }
                bb.rewind(); bb
            }
            else -> {
                throw IllegalArgumentException("Unsupported input dtype: ${spec.dt}. Re-export model as FLOAT32 or UINT8.")
            }
        }
    }

    private fun outputFloats(interp: Interpreter): FloatArray {
        val outShape = interp.getOutputTensor(0).shape() // [1,N]
        val n = outShape[1]
        return FloatArray(n)
    }

    /** ROI față -> (emo, gen, vârstă) */
    fun predictAll(faceBmp: Bitmap): Triple<String,String,Int> {
        // Log input specs o singură dată
        if (BuildConfig.DEBUG) {
            try {
                Log.d(TAG, "EMO in=${emo.getInputTensor(0).shape().contentToString()} ${emo.getInputTensor(0).dataType()}")
                Log.d(TAG, "GEN in=${gen.getInputTensor(0).shape().contentToString()} ${gen.getInputTensor(0).dataType()}")
                Log.d(TAG, "AGE in=${age.getInputTensor(0).shape().contentToString()} ${age.getInputTensor(0).dataType()}")
                Log.d(TAG, "EMO out=${emo.getOutputTensor(0).shape().contentToString()}")
                Log.d(TAG, "GEN out=${gen.getOutputTensor(0).shape().contentToString()}")
                Log.d(TAG, "AGE out=${age.getOutputTensor(0).shape().contentToString()}")
            } catch (_: Throwable) {}
        }

        // EMOTION
        val emoSpec = inputSpec(emo)
        val emoIn = makeInput(faceBmp, emoSpec)
        val emoOut = Array(1) { outputFloats(emo) }
        emo.run(emoIn, emoOut)
        val emoIdx = emoOut[0].indices.maxBy { emoOut[0][it] }
        val emoLabel = EMO[min(emoIdx, EMO.lastIndex)]

        // GENDER
        val genSpec = inputSpec(gen)
        val genIn = makeInput(faceBmp, genSpec)
        val genOut = Array(1) { outputFloats(gen) }
        gen.run(genIn, genOut)
        val gender = when (genOut[0].size) {
            2 -> if (genOut[0][0] > genOut[0][1]) "Woman" else "Man"
            1 -> if (genOut[0][0] >= 0.5f) "Man" else "Woman"
            else -> "Unknown"
        }

        // AGE
        val ageSpec = inputSpec(age)
        val ageIn = makeInput(faceBmp, ageSpec)
        val ageOutArr = Array(1) { outputFloats(age) }
        age.run(ageIn, ageOutArr)
        val ageVec = ageOutArr[0]
        val ageInt = when (ageVec.size) {
            1 -> ageVec[0].toInt().coerceIn(0, 100)
            101 -> {
                var sum = 0.0
                for (i in 0..100) sum += i * ageVec[i]
                sum.toInt().coerceIn(0, 100)
            }
            else -> ageVec.indices.maxBy { ageVec[it] }.coerceIn(0, 100)
        }

        return Triple(emoLabel, gender, ageInt)
    }
}
