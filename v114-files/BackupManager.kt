package com.aboryan.rased.albarr

import android.content.Context
import android.net.Uri
import org.json.JSONArray
import org.json.JSONObject
import java.io.BufferedInputStream
import java.io.BufferedOutputStream
import java.io.File
import java.io.FileInputStream
import java.io.InputStream
import java.util.zip.ZipEntry
import java.util.zip.ZipInputStream
import java.util.zip.ZipOutputStream

class BackupManager(private val context: Context, private val db: ObservationDb) {

    fun exportTo(uri: Uri) {
        val items = db.all()
        val jsonItems = JSONArray()
        val sources = mutableListOf<Pair<String, String>>()

        items.forEach { o ->
            val imageEntries = JSONArray()
            o.allImages().forEachIndexed { index, imageUri ->
                if (canOpen(imageUri)) {
                    val entryName = "images/${o.id}_${index}.img"
                    sources += entryName to imageUri
                    imageEntries.put(entryName)
                }
            }
            jsonItems.put(JSONObject().apply {
                put("id", o.id)
                put("title", o.title)
                put("category", o.category)
                put("rarity", o.rarity)
                put("description", o.description)
                put("notes", o.notes)
                put("imageUri", o.imageUri)
                put("imageEntries", imageEntries)
                if (o.latitude == null) put("latitude", JSONObject.NULL) else put("latitude", o.latitude)
                if (o.longitude == null) put("longitude", JSONObject.NULL) else put("longitude", o.longitude)
                if (o.altitude == null) put("altitude", JSONObject.NULL) else put("altitude", o.altitude)
                if (o.accuracy == null) put("accuracy", JSONObject.NULL) else put("accuracy", o.accuracy.toDouble())
                if (o.locationCapturedAt == null) put("locationCapturedAt", JSONObject.NULL) else put("locationCapturedAt", o.locationCapturedAt)
                put("locationProvider", o.locationProvider)
                put("placeName", o.placeName)
                put("tripName", o.tripName)
                put("tags", o.tags)
                put("createdAt", o.createdAt)
                put("favorite", o.favorite)
                put("quickDraft", o.quickDraft)
            })
        }

        val root = JSONObject().apply {
            put("format", "RasedAlBarrBackup")
            put("version", 2)
            put("createdAt", System.currentTimeMillis())
            put("app", "راصد البرية")
            put("itemCount", items.size)
            put("items", jsonItems)
        }

        context.contentResolver.openOutputStream(uri, "w")?.use { output ->
            ZipOutputStream(BufferedOutputStream(output)).use { zip ->
                zip.putNextEntry(ZipEntry("data.json"))
                zip.write(root.toString().toByteArray(Charsets.UTF_8))
                zip.closeEntry()

                sources.forEach { (entryName, imageUri) ->
                    openImage(imageUri)?.use { input ->
                        zip.putNextEntry(ZipEntry(entryName))
                        input.copyTo(zip, 64 * 1024)
                        zip.closeEntry()
                    }
                }
            }
        } ?: error("تعذر إنشاء ملف النسخة الاحتياطية")
    }

    fun importFrom(uri: Uri): Int {
        var metadata: JSONObject? = null
        val imageDir = File(context.filesDir, "imported_images/${System.currentTimeMillis()}").apply { mkdirs() }
        val imageMap = mutableMapOf<String, String>()

        context.contentResolver.openInputStream(uri)?.use { raw ->
            ZipInputStream(BufferedInputStream(raw)).use { zip ->
                var entry = zip.nextEntry
                while (entry != null) {
                    val safeName = entry.name.replace("..", "").replace('\\', '/')
                    if (!entry.isDirectory && safeName == "data.json") {
                        metadata = JSONObject(zip.readBytes().toString(Charsets.UTF_8))
                    } else if (!entry.isDirectory && safeName.startsWith("images/")) {
                        val base = safeName.substringAfterLast('/').replace(Regex("[^A-Za-z0-9._-]"), "_")
                        val file = File(imageDir, base)
                        BufferedOutputStream(file.outputStream()).use { out -> zip.copyTo(out, 64 * 1024) }
                        imageMap[safeName] = Uri.fromFile(file).toString()
                    }
                    zip.closeEntry()
                    entry = zip.nextEntry
                }
            }
        } ?: error("تعذر فتح ملف النسخة الاحتياطية")

        val root = metadata ?: error("ملف النسخة الاحتياطية غير صالح")
        if (root.optString("format") != "RasedAlBarrBackup") error("صيغة النسخة الاحتياطية غير مدعومة")
        val version = root.optInt("version", 1)
        val arr = root.getJSONArray("items")
        val items = ArrayList<Observation>(arr.length())

        for (i in 0 until arr.length()) {
            val j = arr.getJSONObject(i)
            val restoredImages = mutableListOf<String>()
            if (version >= 2) {
                val entries = j.optJSONArray("imageEntries")
                if (entries != null) {
                    for (x in 0 until entries.length()) {
                        val key = entries.optString(x)
                        imageMap[key]?.let(restoredImages::add)
                    }
                }
            } else {
                val entry = j.optString("imageEntry")
                imageMap[entry]?.let(restoredImages::add)
            }
            if (restoredImages.isEmpty()) j.optString("imageUri").takeIf { it.isNotBlank() && canOpen(it) }?.let(restoredImages::add)

            items += Observation(
                id = j.optLong("id"),
                title = j.optString("title"),
                category = j.optString("category", "أخرى"),
                rarity = j.optString("rarity", "ملفت"),
                description = j.optString("description"),
                notes = j.optString("notes"),
                imageUri = restoredImages.firstOrNull().orEmpty(),
                imageUris = restoredImages,
                latitude = nullableDouble(j, "latitude"),
                longitude = nullableDouble(j, "longitude"),
                altitude = nullableDouble(j, "altitude"),
                accuracy = nullableDouble(j, "accuracy")?.toFloat(),
                locationCapturedAt = nullableLong(j, "locationCapturedAt"),
                locationProvider = j.optString("locationProvider"),
                placeName = j.optString("placeName"),
                tripName = j.optString("tripName"),
                tags = j.optString("tags"),
                createdAt = j.optLong("createdAt", System.currentTimeMillis()),
                favorite = j.optBoolean("favorite"),
                quickDraft = j.optBoolean("quickDraft", false)
            )
        }
        db.replaceAll(items)
        return items.size
    }

    private fun nullableDouble(j: JSONObject, key: String): Double? = if (!j.has(key) || j.isNull(key)) null else j.optDouble(key)
    private fun nullableLong(j: JSONObject, key: String): Long? = if (!j.has(key) || j.isNull(key)) null else j.optLong(key)

    private fun canOpen(uriString: String): Boolean = try {
        openImage(uriString)?.use { true } ?: false
    } catch (_: Exception) { false }

    private fun openImage(uriString: String): InputStream? {
        if (uriString.isBlank()) return null
        val uri = Uri.parse(uriString)
        return when (uri.scheme) {
            "file" -> FileInputStream(File(requireNotNull(uri.path)))
            else -> context.contentResolver.openInputStream(uri)
        }
    }
}
