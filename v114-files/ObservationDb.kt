package com.aboryan.rased.albarr

import android.content.ContentValues
import android.content.Context
import android.database.Cursor
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import org.json.JSONArray

class ObservationDb(context: Context) : SQLiteOpenHelper(context, DB_NAME, null, DB_VERSION) {
    companion object {
        const val DB_NAME = "marsad_albarr.db"
        private const val DB_VERSION = 2
        private const val TABLE = "observations"
    }

    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL("""
            CREATE TABLE IF NOT EXISTS $TABLE (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL DEFAULT '',
                category TEXT NOT NULL DEFAULT 'أخرى',
                rarity TEXT NOT NULL DEFAULT 'ملفت',
                description TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',
                image_uri TEXT NOT NULL DEFAULT '',
                image_uris TEXT NOT NULL DEFAULT '',
                latitude REAL,
                longitude REAL,
                altitude REAL,
                accuracy REAL,
                location_captured_at INTEGER,
                location_provider TEXT NOT NULL DEFAULT '',
                place_name TEXT NOT NULL DEFAULT '',
                trip_name TEXT NOT NULL DEFAULT '',
                tags TEXT NOT NULL DEFAULT '',
                created_at INTEGER NOT NULL,
                favorite INTEGER NOT NULL DEFAULT 0,
                quick_draft INTEGER NOT NULL DEFAULT 0
            )
        """.trimIndent())
        createIndexes(db)
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        if (oldVersion < 2) {
            addColumn(db, "image_uris TEXT NOT NULL DEFAULT ''")
            addColumn(db, "altitude REAL")
            addColumn(db, "accuracy REAL")
            addColumn(db, "location_captured_at INTEGER")
            addColumn(db, "location_provider TEXT NOT NULL DEFAULT ''")
            addColumn(db, "trip_name TEXT NOT NULL DEFAULT ''")
            addColumn(db, "quick_draft INTEGER NOT NULL DEFAULT 0")
            db.execSQL("UPDATE $TABLE SET image_uris='[]' WHERE image_uris='' OR image_uris IS NULL")
        }
        createIndexes(db)
    }

    private fun addColumn(db: SQLiteDatabase, definition: String) {
        runCatching { db.execSQL("ALTER TABLE $TABLE ADD COLUMN $definition") }
    }

    private fun createIndexes(db: SQLiteDatabase) {
        db.execSQL("CREATE INDEX IF NOT EXISTS idx_observations_created_at ON $TABLE(created_at)")
        db.execSQL("CREATE INDEX IF NOT EXISTS idx_observations_category ON $TABLE(category)")
        db.execSQL("CREATE INDEX IF NOT EXISTS idx_observations_trip ON $TABLE(trip_name)")
    }

    fun save(item: Observation): Long {
        val values = values(item, includeId = false)
        return if (item.id > 0) {
            writableDatabase.update(TABLE, values, "id=?", arrayOf(item.id.toString()))
            item.id
        } else {
            writableDatabase.insertOrThrow(TABLE, null, values)
        }
    }

    fun insertPreservingId(item: Observation) {
        writableDatabase.insertOrThrow(TABLE, null, values(item, includeId = true))
    }

    private fun values(o: Observation, includeId: Boolean): ContentValues = ContentValues().apply {
        if (includeId && o.id > 0) put("id", o.id)
        val images = o.allImages()
        val primary = images.firstOrNull().orEmpty().ifBlank { o.imageUri }
        put("title", o.title)
        put("category", o.category)
        put("rarity", o.rarity)
        put("description", o.description)
        put("notes", o.notes)
        put("image_uri", primary)
        put("image_uris", JSONArray(images).toString())
        if (o.latitude == null) putNull("latitude") else put("latitude", o.latitude)
        if (o.longitude == null) putNull("longitude") else put("longitude", o.longitude)
        if (o.altitude == null) putNull("altitude") else put("altitude", o.altitude)
        if (o.accuracy == null) putNull("accuracy") else put("accuracy", o.accuracy)
        if (o.locationCapturedAt == null) putNull("location_captured_at") else put("location_captured_at", o.locationCapturedAt)
        put("location_provider", o.locationProvider)
        put("place_name", o.placeName)
        put("trip_name", o.tripName)
        put("tags", o.tags)
        put("created_at", o.createdAt)
        put("favorite", if (o.favorite) 1 else 0)
        put("quick_draft", if (o.quickDraft) 1 else 0)
    }

    fun delete(id: Long) = writableDatabase.delete(TABLE, "id=?", arrayOf(id.toString()))

    fun clearAll() {
        writableDatabase.beginTransaction()
        try {
            writableDatabase.delete(TABLE, null, null)
            writableDatabase.execSQL("DELETE FROM sqlite_sequence WHERE name=?", arrayOf(TABLE))
            writableDatabase.setTransactionSuccessful()
        } finally {
            writableDatabase.endTransaction()
        }
    }

    fun replaceAll(items: List<Observation>) {
        writableDatabase.beginTransaction()
        try {
            writableDatabase.delete(TABLE, null, null)
            items.forEach { writableDatabase.insertOrThrow(TABLE, null, values(it, includeId = true)) }
            writableDatabase.setTransactionSuccessful()
        } finally {
            writableDatabase.endTransaction()
        }
    }

    fun get(id: Long): Observation? = readableDatabase.query(
        TABLE, null, "id=?", arrayOf(id.toString()), null, null, null, "1"
    ).use { c -> if (c.moveToFirst()) from(c) else null }

    fun all(): List<Observation> = list("", "الكل", false, "كل الرحلات")

    fun list(query: String, category: String, favoritesOnly: Boolean, trip: String = "كل الرحلات"): List<Observation> {
        val where = mutableListOf<String>()
        val args = mutableListOf<String>()
        if (query.isNotBlank()) {
            where += "(title LIKE ? OR description LIKE ? OR notes LIKE ? OR tags LIKE ? OR place_name LIKE ? OR trip_name LIKE ?)"
            repeat(6) { args += "%$query%" }
        }
        if (category.isNotBlank() && category != "الكل") {
            where += "category=?"; args += category
        }
        if (trip.isNotBlank() && trip != "كل الرحلات") {
            where += "trip_name=?"; args += trip
        }
        if (favoritesOnly) where += "favorite=1"
        return readableDatabase.query(
            TABLE, null,
            where.takeIf { it.isNotEmpty() }?.joinToString(" AND "),
            args.takeIf { it.isNotEmpty() }?.toTypedArray(),
            null, null, "created_at DESC"
        ).use { c -> buildList { while (c.moveToNext()) add(from(c)) } }
    }

    fun byTrip(tripName: String): List<Observation> = if (tripName.isBlank()) emptyList() else list("", "الكل", false, tripName)

    fun tripNames(): List<String> = readableDatabase.rawQuery(
        "SELECT DISTINCT trip_name FROM $TABLE WHERE trim(trip_name) <> '' ORDER BY trip_name COLLATE NOCASE",
        null
    ).use { c -> buildList { while (c.moveToNext()) add(c.getString(0).orEmpty()) } }

    fun tripCounts(): List<Pair<String, Int>> = readableDatabase.rawQuery(
        "SELECT trip_name, COUNT(*) FROM $TABLE WHERE trim(trip_name) <> '' GROUP BY trip_name ORDER BY MAX(created_at) DESC",
        null
    ).use { c -> buildList { while (c.moveToNext()) add(c.getString(0).orEmpty() to c.getInt(1)) } }

    fun totalCount(): Int = scalar("SELECT COUNT(*) FROM $TABLE")
    fun favoriteCount(): Int = scalar("SELECT COUNT(*) FROM $TABLE WHERE favorite=1")
    fun locatedCount(): Int = scalar("SELECT COUNT(*) FROM $TABLE WHERE latitude IS NOT NULL AND longitude IS NOT NULL")
    fun draftCount(): Int = scalar("SELECT COUNT(*) FROM $TABLE WHERE quick_draft=1")

    private fun scalar(sql: String): Int = readableDatabase.rawQuery(sql, null).use { c -> if (c.moveToFirst()) c.getInt(0) else 0 }

    private fun from(c: Cursor): Observation {
        fun idx(name: String) = c.getColumnIndex(name)
        fun string(name: String, fallback: String = ""): String {
            val i = idx(name); return if (i < 0 || c.isNull(i)) fallback else c.getString(i) ?: fallback
        }
        fun nullableDouble(name: String): Double? { val i = idx(name); return if (i < 0 || c.isNull(i)) null else c.getDouble(i) }
        fun nullableFloat(name: String): Float? { val i = idx(name); return if (i < 0 || c.isNull(i)) null else c.getFloat(i) }
        fun nullableLong(name: String): Long? { val i = idx(name); return if (i < 0 || c.isNull(i)) null else c.getLong(i) }
        fun bool(name: String): Boolean { val i = idx(name); return i >= 0 && !c.isNull(i) && c.getInt(i) == 1 }

        val legacyImage = string("image_uri")
        val images = parseImages(string("image_uris"), legacyImage)
        return Observation(
            id = c.getLong(c.getColumnIndexOrThrow("id")),
            title = string("title"),
            category = string("category", "أخرى"),
            rarity = string("rarity", "ملفت"),
            description = string("description"),
            notes = string("notes"),
            imageUri = images.firstOrNull().orEmpty().ifBlank { legacyImage },
            imageUris = images,
            latitude = nullableDouble("latitude"),
            longitude = nullableDouble("longitude"),
            altitude = nullableDouble("altitude"),
            accuracy = nullableFloat("accuracy"),
            locationCapturedAt = nullableLong("location_captured_at"),
            locationProvider = string("location_provider"),
            placeName = string("place_name"),
            tripName = string("trip_name"),
            tags = string("tags"),
            createdAt = nullableLong("created_at") ?: System.currentTimeMillis(),
            favorite = bool("favorite"),
            quickDraft = bool("quick_draft")
        )
    }

    private fun parseImages(json: String, legacy: String): List<String> {
        val out = mutableListOf<String>()
        runCatching {
            if (json.isNotBlank()) {
                val arr = JSONArray(json)
                for (i in 0 until arr.length()) arr.optString(i).takeIf { it.isNotBlank() }?.let(out::add)
            }
        }
        if (legacy.isNotBlank()) {
            out.remove(legacy)
            out.add(0, legacy)
        }
        return out.distinct()
    }
}
