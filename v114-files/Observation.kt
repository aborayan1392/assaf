package com.aboryan.rased.albarr

data class Observation(
    val id: Long = 0L,
    val title: String = "",
    val category: String = "أخرى",
    val rarity: String = "ملفت",
    val description: String = "",
    val notes: String = "",
    val imageUri: String = "",
    val imageUris: List<String> = emptyList(),
    val latitude: Double? = null,
    val longitude: Double? = null,
    val altitude: Double? = null,
    val accuracy: Float? = null,
    val locationCapturedAt: Long? = null,
    val locationProvider: String = "",
    val placeName: String = "",
    val tripName: String = "",
    val tags: String = "",
    val createdAt: Long = System.currentTimeMillis(),
    val favorite: Boolean = false,
    val quickDraft: Boolean = false
) {
    fun allImages(): List<String> {
        val list = imageUris.filter { it.isNotBlank() }.distinct().toMutableList()
        if (imageUri.isNotBlank()) {
            list.remove(imageUri)
            list.add(0, imageUri)
        }
        return list
    }
}
