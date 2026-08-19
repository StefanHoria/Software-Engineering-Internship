package com.example.visiondemo

import android.graphics.*
import androidx.camera.core.ImageProxy
import java.io.ByteArrayOutputStream

fun ImageProxy.toBitmap(): Bitmap {
    val yBuffer = planes[0].buffer
    val uBuffer = planes[1].buffer
    val vBuffer = planes[2].buffer
    val ySize = yBuffer.remaining()
    val uSize = uBuffer.remaining()
    val vSize = vBuffer.remaining()
    val nv21 = ByteArray(ySize + uSize + vSize)
    yBuffer.get(nv21, 0, ySize)
    vBuffer.get(nv21, ySize, vSize)
    uBuffer.get(nv21, ySize + vSize, uSize)
    val yuv = YuvImage(nv21, ImageFormat.NV21, width, height, null)
    val out = ByteArrayOutputStream()
    yuv.compressToJpeg(Rect(0,0,width,height), 90, out)
    val bytes = out.toByteArray()
    return BitmapFactory.decodeByteArray(bytes, 0, bytes.size)
}

fun Bitmap.cropSafe(r: Rect): Bitmap {
    val rr = Rect(
        r.left.coerceAtLeast(0),
        r.top.coerceAtLeast(0),
        r.right.coerceAtMost(width),
        r.bottom.coerceAtMost(height)
    )
    return Bitmap.createBitmap(this, rr.left, rr.top, rr.width(), rr.height())
}
