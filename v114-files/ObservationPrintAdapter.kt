package com.aboryan.rased.albarr

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import android.graphics.Typeface
import android.net.Uri
import android.os.Bundle
import android.os.CancellationSignal
import android.os.ParcelFileDescriptor
import android.print.PageRange
import android.print.PrintAttributes
import android.print.PrintDocumentAdapter
import android.print.PrintDocumentInfo
import android.print.pdf.PrintedPdfDocument
import android.text.Layout
import android.text.StaticLayout
import android.text.TextDirectionHeuristics
import android.text.TextPaint
import android.text.TextUtils
import com.google.zxing.BarcodeFormat
import com.google.zxing.EncodeHintType
import com.google.zxing.qrcode.QRCodeWriter
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.text.SimpleDateFormat
import java.util.Date
import java.util.EnumMap
import java.util.Locale
import kotlin.math.max

class ObservationPrintAdapter(
    private val context: Context,
    private val items: List<Observation>,
    private val jobName: String,
    private val singleMode: Boolean,
    private val typeface: Typeface
) : PrintDocumentAdapter() {

    private var attributes: PrintAttributes? = null
    private val pageCount: Int get() = if (singleMode) max(1, items.size) else max(1, (items.size + 3) / 4)

    override fun onLayout(
        oldAttributes: PrintAttributes?,
        newAttributes: PrintAttributes,
        cancellationSignal: CancellationSignal,
        callback: LayoutResultCallback,
        extras: Bundle?
    ) {
        attributes = newAttributes
        if (cancellationSignal.isCanceled) {
            callback.onLayoutCancelled(); return
        }
        val info = PrintDocumentInfo.Builder(jobName)
            .setContentType(PrintDocumentInfo.CONTENT_TYPE_DOCUMENT)
            .setPageCount(pageCount)
            .build()
        callback.onLayoutFinished(info, oldAttributes != newAttributes)
    }

    override fun onWrite(
        pages: Array<out PageRange>,
        destination: ParcelFileDescriptor,
        cancellationSignal: CancellationSignal,
        callback: WriteResultCallback
    ) {
        val attrs = attributes ?: PrintAttributes.Builder().build()
        val document = PrintedPdfDocument(context, attrs)
        try {
            for (pageIndex in 0 until pageCount) {
                if (cancellationSignal.isCanceled) {
                    callback.onWriteCancelled(); return
                }
                if (!containsPage(pages, pageIndex)) continue
                val page = document.startPage(pageIndex)
                if (singleMode) drawSingle(page.canvas, pageIndex) else drawGrid(page.canvas, pageIndex)
                document.finishPage(page)
            }
            FileOutputStream(destination.fileDescriptor).use { document.writeTo(it) }
            callback.onWriteFinished(pages)
        } catch (e: Exception) {
            callback.onWriteFailed(e.localizedMessage ?: "تعذر إنشاء ملف الطباعة")
        } finally {
            document.close()
        }
    }

    private fun containsPage(ranges: Array<out PageRange>, page: Int): Boolean =
        ranges.any { it == PageRange.ALL_PAGES || page in it.start..it.end }

    private fun drawHeader(canvas: Canvas, title: String) {
        val w = canvas.width.toFloat()
        val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            color = Color.rgb(28, 103, 73)
            textSize = canvas.height * 0.030f
            textAlign = Paint.Align.RIGHT
            typeface = this@ObservationPrintAdapter.typeface
        }
        canvas.drawText(title, w * .94f, canvas.height * .055f, paint)
        paint.color = Color.rgb(200, 141, 74)
        canvas.drawRect(w * .06f, canvas.height * .068f, w * .94f, canvas.height * .071f, paint)
    }

    private fun drawGrid(canvas: Canvas, pageIndex: Int) {
        canvas.drawColor(Color.WHITE)
        drawHeader(canvas, "راصد البرية — سجل الرصد")
        val w = canvas.width.toFloat(); val h = canvas.height.toFloat()
        val margin = w * .055f; val gap = w * .03f
        val top = h * .095f; val bottom = h * .055f
        val cardW = (w - margin * 2 - gap) / 2f
        val cardH = (h - top - bottom - gap) / 2f
        for (slot in 0 until 4) {
            val index = pageIndex * 4 + slot
            if (index >= items.size) break
            val row = slot / 2
            val col = slot % 2
            val left = if (col == 0) w - margin - cardW else margin
            val y = top + row * (cardH + gap)
            drawCard(canvas, items[index], RectF(left, y, left + cardW, y + cardH))
        }
        drawPageNumber(canvas, pageIndex + 1)
    }

    private fun drawCard(canvas: Canvas, item: Observation, rect: RectF) {
        val border = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            style = Paint.Style.STROKE; strokeWidth = rect.width() * .005f; color = Color.rgb(220, 225, 221)
        }
        canvas.drawRoundRect(rect, rect.width() * .035f, rect.width() * .035f, border)
        val pad = rect.width() * .045f
        val imageRect = RectF(rect.left + pad, rect.top + pad, rect.right - pad, rect.top + rect.height() * .52f)
        drawImage(canvas, item.imageUri, imageRect)
        var y = imageRect.bottom + rect.height() * .045f
        y = drawWrapped(canvas, item.title.ifBlank { "بدون عنوان" }, rect.left + pad, y, rect.width() - pad * 2, rect.width() * .061f, Color.rgb(24, 54, 43), 2, true)

        val hasQr = item.latitude != null && item.longitude != null
        val qrSize = if (hasQr) rect.width() * .19f else 0f
        val textLeft = rect.left + pad + if (hasQr) qrSize + rect.width() * .025f else 0f
        val textWidth = rect.right - pad - textLeft
        val location = when {
            item.placeName.isNotBlank() -> item.placeName
            item.latitude != null && item.longitude != null -> String.format(Locale.US, "%.5f, %.5f", item.latitude, item.longitude)
            else -> "بدون موقع"
        }
        val tripLine = item.tripName.takeIf { it.isNotBlank() }?.let { "الرحلة: $it\n" }.orEmpty()
        val gpsLine = gpsSummary(item).takeIf { it.isNotBlank() }?.let { "$it\n" }.orEmpty()
        val meta = "رصد #${item.id}  ·  ${item.category}  ·  ${item.rarity}\n$tripLine$location  ·  ${date(item.createdAt)}\n$gpsLine".trim()
        y = drawWrapped(canvas, meta, textLeft, y + rect.height() * .014f, textWidth, rect.width() * .036f, Color.rgb(98, 113, 107), 4, false)
        if (item.description.isNotBlank()) {
            drawWrapped(canvas, item.description, textLeft, y + rect.height() * .012f, textWidth, rect.width() * .037f, Color.rgb(45, 62, 56), 3, false)
        }
        if (hasQr) {
            val qrRect = RectF(rect.left + pad, rect.bottom - pad - qrSize, rect.left + pad + qrSize, rect.bottom - pad)
            drawQr(canvas, item, qrRect)
        }
    }

    private fun drawSingle(canvas: Canvas, pageIndex: Int) {
        canvas.drawColor(Color.WHITE)
        val item = items.getOrNull(pageIndex) ?: return
        drawHeader(canvas, "راصد البرية — رصد فردي")
        val w = canvas.width.toFloat(); val h = canvas.height.toFloat(); val margin = w * .08f
        val imageRect = RectF(margin, h * .105f, w - margin, h * .53f)
        drawImage(canvas, item.imageUri, imageRect)
        var y = h * .575f
        y = drawWrapped(canvas, item.title, margin, y, w - margin * 2, w * .043f, Color.rgb(24, 54, 43), 2, true)
        val location = when {
            item.placeName.isNotBlank() -> item.placeName
            item.latitude != null && item.longitude != null -> String.format(Locale.US, "%.6f, %.6f", item.latitude, item.longitude)
            else -> "بدون موقع"
        }
        val trip = if (item.tripName.isNotBlank()) "\nالرحلة: ${item.tripName}" else ""
        val gps = gpsSummary(item).takeIf { it.isNotBlank() }?.let { "\n$it" }.orEmpty()
        val meta = "رقم الرصد: #${item.id}\n${item.category}  ·  ${item.rarity}  ·  ${date(item.createdAt)}\nالموقع: $location$trip$gps"
        y = drawWrapped(canvas, meta, margin, y + h * .010f, w - margin * 2, w * .025f, Color.rgb(93, 111, 103), 6, false)
        if (item.description.isNotBlank()) y = drawWrapped(canvas, "الوصف: ${item.description}", margin, y + h * .012f, w - margin * 2, w * .026f, Color.rgb(40, 56, 50), 4, false)
        if (item.notes.isNotBlank()) y = drawWrapped(canvas, "ملاحظات: ${item.notes}", margin, y + h * .008f, w - margin * 2, w * .024f, Color.rgb(55, 70, 65), 3, false)
        if (item.tags.isNotBlank()) drawWrapped(canvas, "الوسوم: ${item.tags}", margin, y + h * .008f, w - margin * 2, w * .023f, Color.rgb(31, 113, 84), 2, false)

        if (item.latitude != null && item.longitude != null) {
            val qrSize = w * .14f
            val qrRect = RectF(margin, h * .805f, margin + qrSize, h * .805f + qrSize)
            drawQr(canvas, item, qrRect)
            val label = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.rgb(31, 113, 84); textSize = w * .020f; textAlign = Paint.Align.CENTER; typeface = this@ObservationPrintAdapter.typeface }
            canvas.drawText("موقع الرصد", qrRect.centerX(), qrRect.bottom + h * .018f, label)
        }
        drawPageNumber(canvas, pageIndex + 1)
    }

    private fun gpsSummary(item: Observation): String {
        val parts = mutableListOf<String>()
        item.accuracy?.let { parts += "الدقة ±${it.toInt()}م" }
        item.altitude?.let { parts += "الارتفاع ${it.toInt()}م" }
        item.locationCapturedAt?.let { parts += "التقاط ${SimpleDateFormat("dd/MM HH:mm", Locale("ar")).format(Date(it))}" }
        return parts.joinToString("  ·  ")
    }

    private fun drawQr(canvas: Canvas, item: Observation, dst: RectF) {
        val lat = item.latitude ?: return
        val lon = item.longitude ?: return
        try {
            val content = "https://maps.google.com/?q=${String.format(Locale.US, "%.6f", lat)},${String.format(Locale.US, "%.6f", lon)}"
            val size = 256
            val hints = EnumMap<EncodeHintType, Any>(EncodeHintType::class.java).apply { put(EncodeHintType.MARGIN, 1) }
            val matrix = QRCodeWriter().encode(content, BarcodeFormat.QR_CODE, size, size, hints)
            val pixels = IntArray(size * size)
            for (y in 0 until size) for (x in 0 until size) pixels[y * size + x] = if (matrix[x, y]) Color.BLACK else Color.WHITE
            val bmp = Bitmap.createBitmap(size, size, Bitmap.Config.ARGB_8888)
            bmp.setPixels(pixels, 0, size, 0, 0, size, size)
            canvas.drawBitmap(bmp, null, dst, Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG))
            bmp.recycle()
        } catch (_: Exception) { }
    }

    private fun drawPageNumber(canvas: Canvas, page: Int) {
        val p = Paint(Paint.ANTI_ALIAS_FLAG).apply {
            textSize = canvas.width * .022f; color = Color.GRAY; textAlign = Paint.Align.CENTER; typeface = this@ObservationPrintAdapter.typeface
        }
        canvas.drawText(page.toString(), canvas.width / 2f, canvas.height * .975f, p)
    }

    private fun drawImage(canvas: Canvas, uriString: String, dst: RectF) {
        val bg = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.rgb(245, 243, 236) }
        canvas.drawRoundRect(dst, dst.width() * .025f, dst.width() * .025f, bg)
        val bmp = decode(uriString) ?: return
        val srcRatio = bmp.width.toFloat() / bmp.height.coerceAtLeast(1)
        val dstRatio = dst.width() / dst.height().coerceAtLeast(1f)
        val src = if (srcRatio > dstRatio) {
            val wanted = (bmp.height * dstRatio).toInt(); val x = (bmp.width - wanted) / 2
            android.graphics.Rect(x, 0, x + wanted, bmp.height)
        } else {
            val wanted = (bmp.width / dstRatio).toInt(); val y = (bmp.height - wanted) / 2
            android.graphics.Rect(0, y, bmp.width, y + wanted)
        }
        canvas.drawBitmap(bmp, src, dst, Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG))
        bmp.recycle()
    }

    private fun decode(uriString: String): Bitmap? {
        if (uriString.isBlank()) return null
        return try {
            val uri = Uri.parse(uriString)
            val input = if (uri.scheme == "file") FileInputStream(File(requireNotNull(uri.path))) else context.contentResolver.openInputStream(uri)
            input?.use { BitmapFactory.decodeStream(it) }
        } catch (_: Exception) { null }
    }

    private fun drawWrapped(
        canvas: Canvas,
        text: String,
        left: Float,
        top: Float,
        width: Float,
        textSize: Float,
        color: Int,
        maxLines: Int,
        bold: Boolean
    ): Float {
        if (text.isBlank() || width <= 4f) return top
        val tp = TextPaint(Paint.ANTI_ALIAS_FLAG).apply {
            this.textSize = textSize
            this.color = color
            typeface = if (bold) Typeface.create(this@ObservationPrintAdapter.typeface, Typeface.BOLD) else this@ObservationPrintAdapter.typeface
        }
        val layout = StaticLayout.Builder.obtain(text, 0, text.length, tp, width.toInt())
            .setAlignment(Layout.Alignment.ALIGN_NORMAL)
            .setTextDirection(TextDirectionHeuristics.RTL)
            .setIncludePad(false)
            .setMaxLines(maxLines)
            .setEllipsize(TextUtils.TruncateAt.END)
            .build()
        canvas.save(); canvas.translate(left, top); layout.draw(canvas); canvas.restore()
        return top + layout.height
    }

    private fun date(ms: Long): String = SimpleDateFormat("dd MMMM yyyy", Locale("ar")).format(Date(ms))
}
