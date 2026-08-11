from pathlib import Path

p = Path('rased-albarr/app/src/main/java/com/aboryan/rased/albarr/MainActivity.kt')
s = p.read_text()

def one(old, new, label):
    global s
    c = s.count(old)
    if c != 1:
        raise SystemExit(f'{label}: expected 1 target, found {c}')
    s = s.replace(old, new)

s = s.replace('import android.widget.FrameLayout\n', 'import android.widget.FrameLayout\nimport android.widget.HorizontalScrollView\n')
s = s.replace('import android.widget.Toast\n', 'import android.widget.Toast\nimport android.webkit.JavascriptInterface\nimport android.webkit.WebView\nimport android.webkit.WebViewClient\n')
one('    private var favoritesOnly = false\n', '    private var favoritesOnly = false\n    private var selectedTrip = "كل الرحلات"\n', 'selected trip state')

one('''    private var editingId = 0L
    private var formImageUri = ""
    private var cameraUri: Uri? = null
    private var formLat: Double? = null
    private var formLon: Double? = null
    private var formImageView: ImageView? = null
    private var locationStatusView: TextView? = null
    private var pendingLocationListener: LocationListener? = null
''', '''    private var editingId = 0L
    private var formImageUri = ""
    private val formImageUris = mutableListOf<String>()
    private var cameraUri: Uri? = null
    private var formLat: Double? = null
    private var formLon: Double? = null
    private var formAltitude: Double? = null
    private var formAccuracy: Float? = null
    private var formLocationCapturedAt: Long? = null
    private var formLocationProvider: String = ""
    private var formImageView: ImageView? = null
    private var formImageStrip: LinearLayout? = null
    private var locationStatusView: TextView? = null
    private var pendingLocationListener: LocationListener? = null
    private var quickCapturePending = false
''', 'form state')

one('''    private fun showHome() {
        currentScreen = "home"
        val root = rootLayout()
''', '''    private fun showHome() {
        currentScreen = "home"
        if (selectedTrip != "كل الرحلات" && selectedTrip !in db.tripNames()) selectedTrip = "كل الرحلات"
        val root = rootLayout()
''', 'home trip validation')
one('val items = db.list(searchQuery, selectedCategory, favoritesOnly)', 'val items = db.list(searchQuery, selectedCategory, favoritesOnly, selectedTrip)', 'trip list filter')

one('''        val add = actionButton("إضافة رصد جديد", R.drawable.ic_add, GREEN, Color.WHITE).apply { setOnClickListener { showForm(null) } }
        body.addView(add, LinearLayout.LayoutParams(-1, dp(54)).apply { setMargins(0, dp(8), 0, dp(6)) })
''', '''        val addRow = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL }
        val add = actionButton("إضافة رصد", R.drawable.ic_add, GREEN, Color.WHITE).apply { setOnClickListener { showForm(null) } }
        val quick = actionButton("رصد سريع", R.drawable.ic_camera, TEAL, Color.WHITE).apply { setOnClickListener { startQuickCapture() } }
        addRow.addView(add, LinearLayout.LayoutParams(0, dp(54), 1f).apply { marginEnd = dp(5) })
        addRow.addView(quick, LinearLayout.LayoutParams(0, dp(54), 1f).apply { marginStart = dp(5) })
        body.addView(addRow, LinearLayout.LayoutParams(-1, dp(54)).apply { setMargins(0, dp(8), 0, dp(6)) })
''', 'quick capture button')

one('''        filters.addView(fav, LinearLayout.LayoutParams(0, dp(54), 1f).apply { marginStart = dp(6) })
        body.addView(filters)
        return body
''', '''        filters.addView(fav, LinearLayout.LayoutParams(0, dp(54), 1f).apply { marginStart = dp(6) })
        body.addView(filters)

        if (db.tripNames().isNotEmpty()) {
            val tripFilter = actionButton("الرحلة: $selectedTrip", R.drawable.ic_explore, Color.rgb(243, 248, 245), GREEN).apply {
                background = rounded(Color.rgb(247, 250, 248), 15f, strokeColor = Color.rgb(205, 222, 214))
                setOnClickListener { showTripFilterDialog() }
            }
            body.addView(tripFilter, LinearLayout.LayoutParams(-1, dp(46)).apply { topMargin = dp(6) })
        }
        return body
''', 'trip filter UI')

one('''        val image = ImageView(this).apply { scaleType = ImageView.ScaleType.CENTER_CROP; background = rounded(Color.rgb(238, 240, 236), 20f); loadImage(this, item.imageUri) }
        body.addView(image, LinearLayout.LayoutParams(-1, dp(280)))
''', '''        val detailImage = ImageView(this).apply { scaleType = ImageView.ScaleType.CENTER_CROP; background = rounded(Color.rgb(238, 240, 236), 20f); loadImage(this, item.imageUri) }
        body.addView(detailImage, LinearLayout.LayoutParams(-1, dp(280)))
        val detailImages = item.allImages()
        if (detailImages.size > 1) {
            val strip = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; setPadding(0, dp(8), 0, dp(2)) }
            detailImages.forEach { uri ->
                val thumb = ImageView(this).apply {
                    scaleType = ImageView.ScaleType.CENTER_CROP; background = rounded(Color.rgb(238, 240, 236), 10f); loadImage(this, uri)
                    setOnClickListener { loadImage(detailImage, uri) }
                }
                strip.addView(thumb, LinearLayout.LayoutParams(dp(72), dp(72)).apply { marginEnd = dp(7) })
            }
            val hs = HorizontalScrollView(this).apply { isHorizontalScrollBarEnabled = false; addView(strip) }
            body.addView(hs, LinearLayout.LayoutParams(-1, dp(84)))
        }
''', 'detail images')

one('''        if (item.notes.isNotBlank()) body.addView(infoBlock("الملاحظات", item.notes))
        if (item.tags.isNotBlank()) body.addView(infoBlock("الوسوم", item.tags))
        val loc = when {
''', '''        if (item.notes.isNotBlank()) body.addView(infoBlock("الملاحظات", item.notes))
        if (item.tags.isNotBlank()) body.addView(infoBlock("الوسوم", item.tags))
        if (item.tripName.isNotBlank()) body.addView(infoBlock("الرحلة", item.tripName))
        if (item.quickDraft) body.addView(infoBlock("حالة الرصد", "مسودة رصد سريع — افتح التعديل لإكمال البيانات"))
        val loc = when {
''', 'detail trip')
one('''        body.addView(infoBlock("الموقع", loc))
        body.addView(infoBlock("تاريخ الرصد", dateTime(item.createdAt)))
''', '''        body.addView(infoBlock("الموقع", loc))
        val gpsDetails = gpsDetailsText(item)
        if (gpsDetails.isNotBlank()) body.addView(infoBlock("بيانات GPS", gpsDetails))
        body.addView(infoBlock("تاريخ الرصد", dateTime(item.createdAt)))
''', 'detail gps')

one('''        editingId = existing?.id ?: 0L
        formImageUri = existing?.imageUri.orEmpty()
        formLat = existing?.latitude
        formLon = existing?.longitude
''', '''        editingId = existing?.id ?: 0L
        formImageUris.clear()
        formImageUris.addAll(existing?.allImages().orEmpty())
        formImageUri = formImageUris.firstOrNull().orEmpty()
        formLat = existing?.latitude
        formLon = existing?.longitude
        formAltitude = existing?.altitude
        formAccuracy = existing?.accuracy
        formLocationCapturedAt = existing?.locationCapturedAt
        formLocationProvider = existing?.locationProvider.orEmpty()
''', 'form init')

one('''        body.addView(formImageView, LinearLayout.LayoutParams(-1, dp(245)))
        val imageButtons = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; setPadding(0, dp(10), 0, dp(10)) }
''', '''        body.addView(formImageView, LinearLayout.LayoutParams(-1, dp(245)))
        formImageStrip = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; setPadding(0, dp(7), 0, 0) }
        val imageScroll = HorizontalScrollView(this).apply { isHorizontalScrollBarEnabled = false; addView(formImageStrip) }
        body.addView(imageScroll, LinearLayout.LayoutParams(-1, dp(76)))
        body.addView(text("يمكن إضافة عدة صور — اضغط الصورة لجعلها الرئيسية، واضغط مطولًا لحذفها", 11.5f, MUTED, false).apply { gravity = Gravity.RIGHT }, LinearLayout.LayoutParams(-1, -2))
        refreshFormImages()
        val imageButtons = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; setPadding(0, dp(8), 0, dp(10)) }
''', 'form image strip')

one('''        val notes = input(body, "ملاحظات ميدانية", "أي ملاحظات إضافية", true, existing?.notes.orEmpty())
        val place = input(body, "اسم المكان", "مثال: وادي، جبل، طريق...", false, existing?.placeName.orEmpty())
''', '''        val notes = input(body, "ملاحظات ميدانية", "أي ملاحظات إضافية", true, existing?.notes.orEmpty())
        val lastTrip = getSharedPreferences("rased_prefs", MODE_PRIVATE).getString("last_trip", "").orEmpty()
        val trip = input(body, "الرحلة (اختياري)", "مثال: رحلة بلجرشي — أغسطس 2026", false, existing?.tripName ?: lastTrip)
        val place = input(body, "اسم المكان", "مثال: وادي، جبل، طريق...", false, existing?.placeName.orEmpty())
''', 'trip input')

one('''        locBox.addView(locationStatusView)
        locBox.addView(actionButton("التقط إحداثياتي الآن", R.drawable.ic_location, TEAL, Color.WHITE).apply { setOnClickListener { requestLocation() } }, LinearLayout.LayoutParams(-1, dp(52)).apply { topMargin = dp(8) })
        body.addView(locBox, LinearLayout.LayoutParams(-1, -2).apply { bottomMargin = dp(10) })
''', '''        locBox.addView(locationStatusView)
        val locButtons = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL }
        locButtons.addView(actionButton("GPS الآن", R.drawable.ic_location, TEAL, Color.WHITE).apply { setOnClickListener { requestLocation() } }, LinearLayout.LayoutParams(0, dp(52), 1f).apply { marginEnd = dp(5) })
        locButtons.addView(actionButton("تحديد يدوي", R.drawable.ic_explore, GREEN, Color.WHITE).apply { setOnClickListener { showManualLocationPicker() } }, LinearLayout.LayoutParams(0, dp(52), 1f).apply { marginStart = dp(5) })
        locBox.addView(locButtons, LinearLayout.LayoutParams(-1, dp(52)).apply { topMargin = dp(8) })
        body.addView(locBox, LinearLayout.LayoutParams(-1, -2).apply { bottomMargin = dp(10) })
''', 'manual location buttons')

one('''                notes = notes.text.toString().trim(),
                imageUri = formImageUri,
                latitude = formLat,
                longitude = formLon,
                placeName = place.text.toString().trim(),
                tags = tags.text.toString().trim(),
                createdAt = existing?.createdAt ?: System.currentTimeMillis(),
                favorite = favorite.isChecked
''', '''                notes = notes.text.toString().trim(),
                imageUri = formImageUris.firstOrNull().orEmpty(),
                imageUris = formImageUris.toList(),
                latitude = formLat,
                longitude = formLon,
                altitude = formAltitude,
                accuracy = formAccuracy,
                locationCapturedAt = formLocationCapturedAt,
                locationProvider = formLocationProvider,
                placeName = place.text.toString().trim(),
                tripName = trip.text.toString().trim(),
                tags = tags.text.toString().trim(),
                createdAt = existing?.createdAt ?: System.currentTimeMillis(),
                favorite = favorite.isChecked,
                quickDraft = false
''', 'save new fields')
one('''            val id = db.save(o)
            toast("تم حفظ الرصد")
''', '''            val id = db.save(o)
            if (o.tripName.isNotBlank()) getSharedPreferences("rased_prefs", MODE_PRIVATE).edit().putString("last_trip", o.tripName).apply()
            toast("تم حفظ الرصد")
''', 'remember trip')

s = s.replace('"تصدير نسخة احتياطية", "يحفظ البيانات والصور في ملف واحد"', '"تصدير نسخة احتياطية كاملة ZIP", "يحفظ جميع البيانات والصور المتعددة والرحلات في ملف واحد"')
s = s.replace('"استيراد نسخة احتياطية", "يستبدل البيانات الحالية بمحتويات النسخة"', '"استيراد نسخة احتياطية", "يعيد البيانات والصور والرحلات من النسخة الكاملة"')
one('''        wrap.addView(settingsRow(R.drawable.ic_print, "طباعة جماعية", "شبكة عربية مرتبة بصور واضحة — 4 أرصاد في الصفحة", GOLD) {
            dialog.dismiss(); val items = db.all(); if (items.isEmpty()) toast("لا توجد بيانات للطباعة") else printItems(items, false)
        })
        wrap.addView(settingsRow(R.drawable.ic_delete, "مسح كل البيانات", "حذف جميع الأرصاد نهائيًا", RED) {
''', '''        wrap.addView(settingsRow(R.drawable.ic_print, "طباعة جماعية", "شبكة عربية مرتبة بصور واضحة — 4 أرصاد في الصفحة", GOLD) {
            dialog.dismiss(); val items = db.all(); if (items.isEmpty()) toast("لا توجد بيانات للطباعة") else printItems(items, false)
        })
        if (db.tripNames().isNotEmpty()) {
            wrap.addView(settingsRow(R.drawable.ic_explore, "طباعة رحلة", "اختر رحلة لطباعة أرصادها كتقرير واحد", GREEN) {
                dialog.dismiss(); showTripPrintDialog()
            })
        }
        wrap.addView(settingsRow(R.drawable.ic_delete, "مسح كل البيانات", "حذف جميع الأرصاد نهائيًا", RED) {
''', 'trip printing settings')
s = s.replace('text("الإصدار 1.0.8"', 'text("الإصدار 1.0.14"')
s = s.replace('putExtra(Intent.EXTRA_TITLE, "RasedAlBarr_Backup_$stamp.rasedbackup")', 'putExtra(Intent.EXTRA_TITLE, "RasedAlBarr_FullBackup_$stamp.zip")')
s = s.replace('db.clearAll(); toast("تم مسح جميع البيانات"); showHome()', 'db.clearAll(); runCatching { java.io.File(filesDir, "imported_images").deleteRecursively() }; toast("تم مسح جميع البيانات"); showHome()')

one('''    private fun startCamera() {
        val needed = mutableListOf<String>()
''', '''    private fun startCamera() {
        quickCapturePending = false
        val needed = mutableListOf<String>()
''', 'normal camera mode')
s = s.replace('val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply { addCategory(Intent.CATEGORY_OPENABLE); type = "image/*" }', 'val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply { addCategory(Intent.CATEGORY_OPENABLE); type = "image/*"; putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true) }')

one('''    private fun applyLocation(location: Location) {
        formLat = location.latitude; formLon = location.longitude; locationStatusView?.text = locationText(); toast("تم تسجيل الإحداثيات")
    }

    private fun locationText(): String = if (formLat != null && formLon != null) String.format(Locale.US, "%.6f, %.6f", formLat, formLon) else "لم يتم تسجيل إحداثيات بعد"
''', '''    private fun applyLocation(location: Location) {
        formLat = location.latitude
        formLon = location.longitude
        formAltitude = if (location.hasAltitude()) location.altitude else null
        formAccuracy = if (location.hasAccuracy()) location.accuracy else null
        formLocationCapturedAt = if (location.time > 0L) location.time else System.currentTimeMillis()
        formLocationProvider = location.provider.orEmpty()
        locationStatusView?.text = locationText()
        toast("تم تسجيل الإحداثيات — ${locationQuality(formAccuracy)}")
    }

    private fun locationText(): String {
        if (formLat == null || formLon == null) return "لم يتم تسجيل إحداثيات بعد"
        val first = String.format(Locale.US, "%.6f, %.6f", formLat, formLon)
        val parts = mutableListOf<String>()
        formAccuracy?.let { parts += "الدقة ±${it.toInt()} م" }
        formAltitude?.let { parts += "الارتفاع ${it.toInt()} م" }
        if (formAccuracy != null) parts += locationQuality(formAccuracy)
        return if (parts.isEmpty()) first else "$first\\n${parts.joinToString("  ·  ")}"
    }
''', 'gps metadata capture')

s = s.replace('REQ_CAMERA -> if (grantResults.isNotEmpty() && grantResults.all { it == PackageManager.PERMISSION_GRANTED }) launchCameraIntent() else toast("يجب السماح للكاميرا")', 'REQ_CAMERA -> if (grantResults.isNotEmpty() && grantResults.all { it == PackageManager.PERMISSION_GRANTED }) launchCameraIntent() else { quickCapturePending = false; toast("يجب السماح للكاميرا") }')
one('''        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode != RESULT_OK) return
''', '''        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode != RESULT_OK) {
            if (requestCode == REQ_CAMERA) quickCapturePending = false
            return
        }
''', 'cancel quick capture')
one('''            REQ_CAMERA -> {
                cameraUri?.let { formImageUri = it.toString(); formImageView?.let { iv -> loadImage(iv, formImageUri) } }
            }
            REQ_GALLERY -> {
                data?.data?.let { uri ->
                    runCatching { contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION) }
                    formImageUri = uri.toString(); formImageView?.let { iv -> loadImage(iv, formImageUri) }
                }
            }
''', '''            REQ_CAMERA -> {
                cameraUri?.let { uri ->
                    if (quickCapturePending) {
                        quickCapturePending = false
                        saveQuickObservation(uri.toString())
                    } else {
                        addFormImage(uri.toString())
                    }
                }
            }
            REQ_GALLERY -> {
                val uris = mutableListOf<Uri>()
                data?.clipData?.let { clip -> for (i in 0 until clip.itemCount) uris += clip.getItemAt(i).uri }
                if (uris.isEmpty()) data?.data?.let(uris::add)
                uris.distinct().forEach { uri ->
                    runCatching { contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION) }
                    addFormImage(uri.toString())
                }
            }
''', 'multi image results')

marker = '    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {\n'
if marker not in s:
    raise SystemExit('permission marker missing')
helpers = r'''    private fun locationQuality(accuracy: Float?): String = when {
        accuracy == null -> "دقة غير محددة"
        accuracy <= 10f -> "دقة ممتازة"
        accuracy <= 30f -> "دقة جيدة"
        accuracy <= 100f -> "دقة مقبولة"
        else -> "دقة ضعيفة"
    }

    private fun gpsDetailsText(item: Observation): String {
        val lines = mutableListOf<String>()
        item.accuracy?.let { lines += "الدقة: ±${it.toInt()} متر — ${locationQuality(it)}" }
        item.altitude?.let { lines += "الارتفاع عن سطح البحر: ${it.toInt()} متر" }
        item.locationCapturedAt?.let { lines += "وقت التقاط الموقع: ${dateTime(it)}" }
        item.locationProvider.takeIf { it.isNotBlank() }?.let { lines += "مصدر الموقع: ${if (it == "manual") "يدوي" else it}" }
        return lines.joinToString("\n")
    }

    private fun addFormImage(uriString: String) {
        if (uriString.isBlank()) return
        if (uriString !in formImageUris) formImageUris += uriString
        if (formImageUris.isNotEmpty()) formImageUri = formImageUris.first()
        refreshFormImages()
    }

    private fun refreshFormImages() {
        formImageUri = formImageUris.firstOrNull().orEmpty()
        formImageView?.let { loadImage(it, formImageUri) }
        val strip = formImageStrip ?: return
        strip.removeAllViews()
        formImageUris.toList().forEach { uri ->
            val thumb = ImageView(this).apply {
                scaleType = ImageView.ScaleType.CENTER_CROP
                background = rounded(if (uri == formImageUri) Color.rgb(225, 242, 235) else Color.rgb(238, 240, 236), 10f, strokeColor = if (uri == formImageUri) GREEN else Color.rgb(220, 224, 220), strokeWidth = if (uri == formImageUri) 2 else 1)
                loadImage(this, uri)
                setOnClickListener {
                    formImageUris.remove(uri)
                    formImageUris.add(0, uri)
                    refreshFormImages()
                }
                setOnLongClickListener {
                    formImageUris.remove(uri)
                    refreshFormImages()
                    toast("تم حذف الصورة من الرصد")
                    true
                }
            }
            strip.addView(thumb, LinearLayout.LayoutParams(dp(66), dp(66)).apply { marginEnd = dp(7) })
        }
        if (formImageUris.isEmpty()) strip.addView(text("لا توجد صور مضافة", 12f, MUTED, false).apply { gravity = Gravity.CENTER_VERTICAL }, LinearLayout.LayoutParams(-2, dp(66)))
    }

    private fun startQuickCapture() {
        quickCapturePending = true
        val needed = mutableListOf<String>()
        if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) needed += Manifest.permission.CAMERA
        if (Build.VERSION.SDK_INT <= 28 && checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) needed += Manifest.permission.WRITE_EXTERNAL_STORAGE
        if (needed.isNotEmpty()) requestPermissions(needed.toTypedArray(), REQ_CAMERA) else launchCameraIntent()
    }

    private fun bestKnownLocation(maxAgeMs: Long = 30 * 60 * 1000L): Location? {
        val fine = checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
        val coarse = checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED
        if (!fine && !coarse) return null
        val lm = getSystemService(LOCATION_SERVICE) as LocationManager
        val now = System.currentTimeMillis()
        return runCatching {
            lm.allProviders.distinct().mapNotNull { provider -> runCatching { lm.getLastKnownLocation(provider) }.getOrNull() }
                .filter { it.latitude in -90.0..90.0 && it.longitude in -180.0..180.0 && now - it.time in 0..maxAgeMs }
                .sortedWith(compareByDescending<Location> { it.time }.thenBy { if (it.hasAccuracy()) it.accuracy else 99999f })
                .firstOrNull()
        }.getOrNull()
    }

    private fun saveQuickObservation(imageUri: String) {
        val loc = bestKnownLocation()
        val now = System.currentTimeMillis()
        val trip = getSharedPreferences("rased_prefs", MODE_PRIVATE).getString("last_trip", "").orEmpty()
        val title = "رصد سريع - ${SimpleDateFormat("dd MMM HH:mm", Locale("ar")).format(Date(now))}"
        val item = Observation(title = title, category = "أخرى", rarity = "ملفت", imageUri = imageUri, imageUris = listOf(imageUri), latitude = loc?.latitude, longitude = loc?.longitude, altitude = loc?.takeIf { it.hasAltitude() }?.altitude, accuracy = loc?.takeIf { it.hasAccuracy() }?.accuracy, locationCapturedAt = loc?.time?.takeIf { it > 0L }, locationProvider = loc?.provider.orEmpty(), tripName = trip, createdAt = now, quickDraft = true)
        val id = db.save(item)
        if (loc != null) toast("تم حفظ الرصد السريع مع الموقع كمسودة") else toast("تم حفظ الرصد السريع كمسودة — أكمل الموقع لاحقًا")
        showDetail(id)
    }

    private fun showTripFilterDialog() {
        val options = listOf("كل الرحلات") + db.tripNames()
        val checked = options.indexOf(selectedTrip).coerceAtLeast(0)
        AlertDialog.Builder(this).setTitle("تصفية حسب الرحلة").setSingleChoiceItems(options.toTypedArray(), checked) { dialog, which -> selectedTrip = options[which]; dialog.dismiss(); showHome() }.setNegativeButton("إلغاء", null).show()
    }

    private fun showTripPrintDialog() {
        val trips = db.tripNames()
        if (trips.isEmpty()) { toast("لا توجد رحلات مسجلة"); return }
        AlertDialog.Builder(this).setTitle("اختر الرحلة للطباعة").setItems(trips.toTypedArray()) { _, which ->
            val items = db.byTrip(trips[which])
            if (items.isEmpty()) toast("لا توجد أرصاد في هذه الرحلة") else printItems(items, false)
        }.setNegativeButton("إلغاء", null).show()
    }

    private fun showManualLocationPicker() {
        val dialog = Dialog(this)
        val wrap = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(dp(14), dp(14), dp(14), dp(14)); background = rounded(Color.WHITE, 22f) }
        wrap.addView(text("تحديد الموقع يدويًا", 22f, INK, true).apply { gravity = Gravity.RIGHT })
        wrap.addView(text("اضغط على الخريطة لتحديد النقطة، أو اكتب الإحداثيات يدويًا إذا لم تتوفر الإنترنت.", 12.5f, MUTED, false).apply { gravity = Gravity.RIGHT; setPadding(0, dp(4), 0, dp(8)) })
        val latEdit = EditText(this).apply { hint = "خط العرض"; textSize = 14f; setTextColor(INK); setHintTextColor(MUTED); typeface = appTypeface; inputType = InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_FLAG_DECIMAL or InputType.TYPE_NUMBER_FLAG_SIGNED; gravity = Gravity.CENTER; background = rounded(Color.rgb(250,250,248), 13f, strokeColor = Color.rgb(220,222,218)); setPadding(dp(8),0,dp(8),0); formLat?.let { setText(String.format(Locale.US, "%.6f", it)) } }
        val lonEdit = EditText(this).apply { hint = "خط الطول"; textSize = 14f; setTextColor(INK); setHintTextColor(MUTED); typeface = appTypeface; inputType = InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_FLAG_DECIMAL or InputType.TYPE_NUMBER_FLAG_SIGNED; gravity = Gravity.CENTER; background = rounded(Color.rgb(250,250,248), 13f, strokeColor = Color.rgb(220,222,218)); setPadding(dp(8),0,dp(8),0); formLon?.let { setText(String.format(Locale.US, "%.6f", it)) } }
        val coords = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL }
        coords.addView(latEdit, LinearLayout.LayoutParams(0, dp(48), 1f).apply { marginEnd = dp(5) }); coords.addView(lonEdit, LinearLayout.LayoutParams(0, dp(48), 1f).apply { marginStart = dp(5) }); wrap.addView(coords, LinearLayout.LayoutParams(-1, dp(48)).apply { bottomMargin = dp(8) })
        val centerLat = formLat ?: 24.7136; val centerLon = formLon ?: 46.6753
        val web = WebView(this).apply { settings.javaScriptEnabled = true; settings.domStorageEnabled = true; webViewClient = WebViewClient(); addJavascriptInterface(object { @JavascriptInterface fun pick(lat: Double, lon: Double) { runOnUiThread { latEdit.setText(String.format(Locale.US, "%.6f", lat)); lonEdit.setText(String.format(Locale.US, "%.6f", lon)) } } }, "Android") }
        val html = """<!doctype html><html dir="rtl"><head><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/><style>html,body,#map{height:100%;margin:0}.leaflet-control-attribution{font-size:8px}</style></head><body><div id="map"></div><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script><script>var map=L.map('map').setView([$centerLat,$centerLon], ${if (formLat != null) 15 else 5});L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'© OpenStreetMap'}).addTo(map);var marker=L.marker([$centerLat,$centerLon]).addTo(map);map.on('click',function(e){marker.setLatLng(e.latlng);if(window.Android){Android.pick(e.latlng.lat,e.latlng.lng);}});</script></body></html>"""
        web.loadDataWithBaseURL("https://unpkg.com/", html, "text/html", "UTF-8", null); wrap.addView(web, LinearLayout.LayoutParams(-1, dp(310)).apply { bottomMargin = dp(8) })
        val actions = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER }
        val cancel = actionButton("إلغاء", R.drawable.ic_arrow_back, Color.rgb(238,240,236), INK).apply { setOnClickListener { dialog.dismiss() } }
        val save = actionButton("اعتماد الموقع", R.drawable.ic_location, GREEN, Color.WHITE).apply { setOnClickListener { val lat = latEdit.text.toString().trim().toDoubleOrNull(); val lon = lonEdit.text.toString().trim().toDoubleOrNull(); if (lat == null || lon == null || lat !in -90.0..90.0 || lon !in -180.0..180.0) toast("تحقق من صحة خط العرض وخط الطول") else { formLat = lat; formLon = lon; formAltitude = null; formAccuracy = null; formLocationCapturedAt = System.currentTimeMillis(); formLocationProvider = "manual"; locationStatusView?.text = locationText(); toast("تم اعتماد الموقع اليدوي"); dialog.dismiss() } } }
        actions.addView(cancel, LinearLayout.LayoutParams(0, dp(52), 1f).apply { marginEnd = dp(5) }); actions.addView(save, LinearLayout.LayoutParams(0, dp(52), 1f).apply { marginStart = dp(5) }); wrap.addView(actions)
        dialog.setContentView(wrap); dialog.setOnShowListener { dialog.window?.setBackgroundDrawableResource(android.R.color.transparent); dialog.window?.setLayout((resources.displayMetrics.widthPixels * .94f).toInt(), (resources.displayMetrics.heightPixels * .86f).toInt()) }; dialog.show()
    }

'''
s = s.replace(marker, helpers + marker)

assert 'رصد سريع' in s
assert 'imageUris = formImageUris.toList()' in s
assert 'showManualLocationPicker()' in s
assert 'tripName = trip.text.toString().trim()' in s
assert 'formAccuracy = if (location.hasAccuracy()) location.accuracy else null' in s
p.write_text(s)
print('v1.0.14 MainActivity patch applied')
