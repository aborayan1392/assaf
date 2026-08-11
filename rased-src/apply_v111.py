from pathlib import Path

main = Path('rased-albarr/app/src/main/java/com/aboryan/rased/albarr/MainActivity.kt')
s = main.read_text()

# Existing build compatibility and coordinates layout fix.
s = s.replace('ScrollView.LayoutParams(-1, -2)', 'FrameLayout.LayoutParams(-1, -2)')
old_layout = 'body.addView(locBox, fieldLp())'
new_layout = 'body.addView(locBox, LinearLayout.LayoutParams(-1, -2).apply { bottomMargin = dp(10) })'
if s.count(old_layout) != 1:
    raise SystemExit(f'Expected one coordinates layout target, found {s.count(old_layout)}')
s = s.replace(old_layout, new_layout)

# Include IME insets in root bottom padding so keyboard never covers content.
old_insets = '''                val bars = insets.getInsets(WindowInsets.Type.systemBars())
                v.setPadding(bars.left, bars.top, bars.right, bars.bottom)'''
new_insets = '''                val bars = insets.getInsets(WindowInsets.Type.systemBars())
                val ime = insets.getInsets(WindowInsets.Type.ime())
                v.setPadding(bars.left, bars.top, bars.right, maxOf(bars.bottom, ime.bottom))'''
if s.count(old_insets) != 1:
    raise SystemExit(f'Expected one root insets target, found {s.count(old_insets)}')
s = s.replace(old_insets, new_insets)

# Home header: physical left settings button, safe margin; Arabic title stays right aligned.
old_titles = 'frame.addView(titles, FrameLayout.LayoutParams(-1, -1).apply { marginStart = dp(72) })'
new_titles = 'frame.addView(titles, FrameLayout.LayoutParams(-1, -1).apply { marginEnd = dp(82) })'
if s.count(old_titles) != 1:
    raise SystemExit(f'Expected one header titles target, found {s.count(old_titles)}')
s = s.replace(old_titles, new_titles)

old_settings = '''        frame.addView(settings, FrameLayout.LayoutParams(dp(52), dp(52), Gravity.START or Gravity.TOP).apply {
            leftMargin = dp(14); topMargin = dp(16)
        })'''
new_settings = '''        frame.addView(settings, FrameLayout.LayoutParams(dp(56), dp(56), Gravity.LEFT or Gravity.TOP).apply {
            leftMargin = dp(20); topMargin = dp(20)
        })'''
if s.count(old_settings) != 1:
    raise SystemExit(f'Expected one settings target, found {s.count(old_settings)}')
s = s.replace(old_settings, new_settings)

# Form scrolling and focused-field visibility above the IME.
old_scroll = '        val scroll = ScrollView(this).apply { isFillViewport = true }'
new_scroll = '''        val scroll = ScrollView(this).apply {
            isFillViewport = true
            clipToPadding = false
            descendantFocusability = ViewGroup.FOCUS_AFTER_DESCENDANTS
        }'''
if s.count(old_scroll) != 1:
    raise SystemExit(f'Expected one form scroll target, found {s.count(old_scroll)}')
s = s.replace(old_scroll, new_scroll)

old_input = '''            if (multiline) { minLines = 3; inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_MULTI_LINE } else inputType = InputType.TYPE_CLASS_TEXT
        }'''
new_input = '''            if (multiline) { minLines = 3; inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_MULTI_LINE } else inputType = InputType.TYPE_CLASS_TEXT
            setOnFocusChangeListener { v, hasFocus ->
                if (hasFocus) {
                    v.postDelayed({
                        val rect = android.graphics.Rect(0, 0, v.width, v.height + dp(40))
                        v.requestRectangleOnScreen(rect, true)
                    }, 280)
                }
            }
        }'''
if s.count(old_input) != 1:
    raise SystemExit(f'Expected one input helper target, found {s.count(old_input)}')
s = s.replace(old_input, new_input)

# Preserve v1.0.10 location speed/reliability fix.
start = s.index('    private fun captureLocation() {')
end = s.index('    private fun applyLocation(location: Location) {', start)
new_capture = '''    private fun captureLocation() {
        val lm = getSystemService(LOCATION_SERVICE) as LocationManager
        try {
            val fineGranted = checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
            val coarseGranted = checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED
            if (!fineGranted && !coarseGranted) { toast("يجب السماح بالوصول إلى الموقع"); return }

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P && !lm.isLocationEnabled) {
                locationStatusView?.text = "خدمة الموقع متوقفة في الجهاز"
                toast("فعّل خدمة الموقع من إعدادات الجهاز أولًا")
                return
            }

            pendingLocationListener?.let { old -> runCatching { lm.removeUpdates(old) } }
            pendingLocationListener = null

            val now = System.currentTimeMillis()
            val lastLocations = lm.allProviders.distinct()
                .mapNotNull { provider -> runCatching { lm.getLastKnownLocation(provider) }.getOrNull() }
                .filter { it.latitude in -90.0..90.0 && it.longitude in -180.0..180.0 }
                .sortedByDescending { it.time }

            val freshLast = lastLocations.firstOrNull { loc ->
                val age = now - loc.time
                age in 0..(20 * 60 * 1000L) && (!loc.hasAccuracy() || loc.accuracy <= 500f)
            }
            if (freshLast != null) { applyLocation(freshLast); return }

            val networkEnabled = coarseGranted && runCatching { lm.isProviderEnabled(LocationManager.NETWORK_PROVIDER) }.getOrDefault(false)
            val gpsEnabled = fineGranted && runCatching { lm.isProviderEnabled(LocationManager.GPS_PROVIDER) }.getOrDefault(false)
            if (!networkEnabled && !gpsEnabled) {
                locationStatusView?.text = "لا يوجد مزود موقع متاح الآن"
                toast(if (!fineGranted) "فعّل الموقع الدقيق للتطبيق أو شغّل تحديد الموقع عبر الشبكة" else "تأكد من تشغيل خدمة الموقع في الجهاز")
                return
            }

            locationStatusView?.text = when {
                networkEnabled && gpsEnabled -> "جارٍ تحديد الموقع عبر الشبكة وGPS..."
                networkEnabled -> "جارٍ تحديد الموقع عبر الشبكة..."
                else -> "جارٍ تحديد الموقع عبر GPS..."
            }

            var bestCandidate: Location? = lastLocations.firstOrNull { loc ->
                val age = now - loc.time
                age in 0..(30 * 60 * 1000L) && (!loc.hasAccuracy() || loc.accuracy <= 1500f)
            }

            fun isBetter(candidate: Location, current: Location?): Boolean {
                if (current == null) return true
                val candidateAcc = if (candidate.hasAccuracy()) candidate.accuracy else Float.MAX_VALUE
                val currentAcc = if (current.hasAccuracy()) current.accuracy else Float.MAX_VALUE
                return candidate.time > current.time + 5000L || candidateAcc + 20f < currentAcc
            }

            val listener = object : LocationListener {
                override fun onLocationChanged(location: Location) {
                    if (pendingLocationListener !== this) return
                    if (location.latitude !in -90.0..90.0 || location.longitude !in -180.0..180.0) return
                    if (isBetter(location, bestCandidate)) bestCandidate = location
                    val accurateEnough = !location.hasAccuracy() || location.accuracy <= 300f || location.provider == LocationManager.GPS_PROVIDER
                    if (accurateEnough) {
                        runCatching { lm.removeUpdates(this) }
                        pendingLocationListener = null
                        applyLocation(location)
                    }
                }
                @Deprecated("Deprecated in Android") override fun onStatusChanged(provider: String?, status: Int, extras: Bundle?) = Unit
                override fun onProviderEnabled(provider: String) = Unit
                override fun onProviderDisabled(provider: String) = Unit
            }
            pendingLocationListener = listener

            if (networkEnabled) runCatching { lm.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 0L, 0f, listener, Looper.getMainLooper()) }
            if (gpsEnabled) runCatching { lm.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0L, 0f, listener, Looper.getMainLooper()) }

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                if (networkEnabled) runCatching {
                    lm.getCurrentLocation(LocationManager.NETWORK_PROVIDER, null, mainExecutor) { location -> if (location != null) listener.onLocationChanged(location) }
                }
                if (gpsEnabled) runCatching {
                    lm.getCurrentLocation(LocationManager.GPS_PROVIDER, null, mainExecutor) { location -> if (location != null) listener.onLocationChanged(location) }
                }
            }

            Handler(Looper.getMainLooper()).postDelayed({
                if (pendingLocationListener === listener) {
                    runCatching { lm.removeUpdates(listener) }
                    pendingLocationListener = null
                    val fallback = bestCandidate
                    if (fallback != null && now - fallback.time <= 30 * 60 * 1000L) applyLocation(fallback)
                    else {
                        locationStatusView?.text = locationText()
                        toast("لم تصل قراءة موقع بعد؛ تأكد من تشغيل الموقع ثم حاول مرة أخرى")
                    }
                }
            }, 8000)
        } catch (_: SecurityException) {
            locationStatusView?.text = locationText(); toast("صلاحية الموقع غير متاحة للتطبيق")
        } catch (_: Exception) {
            locationStatusView?.text = locationText(); toast("تعذر تشغيل تحديد الموقع، حاول مرة أخرى")
        }
    }

'''
s = s[:start] + new_capture + s[end:]
main.write_text(s)

# Activity keyboard resize hint.
manifest = Path('rased-albarr/app/src/main/AndroidManifest.xml')
ms = manifest.read_text()
old_activity = '''            android:name=".MainActivity"
            android:screenOrientation="unspecified"
            android:exported="true">'''
new_activity = '''            android:name=".MainActivity"
            android:screenOrientation="unspecified"
            android:windowSoftInputMode="adjustResize"
            android:exported="true">'''
if ms.count(old_activity) != 1:
    raise SystemExit(f'Expected one manifest activity target, found {ms.count(old_activity)}')
manifest.write_text(ms.replace(old_activity, new_activity))

# Print adapter compatibility fix retained from v1.0.8 build.
printer = Path('rased-albarr/app/src/main/java/com/aboryan/rased/albarr/ObservationPrintAdapter.kt')
ps = printer.read_text()
old_decode = '''    private fun decode(uriString: String): Bitmap? = try {
        if (uriString.isBlank()) return null
        val uri = Uri.parse(uriString)
        val input = if (uri.scheme == "file") FileInputStream(File(requireNotNull(uri.path))) else context.contentResolver.openInputStream(uri)
        input?.use { BitmapFactory.decodeStream(it) }
    } catch (_: Exception) { null }'''
new_decode = '''    private fun decode(uriString: String): Bitmap? {
        if (uriString.isBlank()) return null
        return try {
            val uri = Uri.parse(uriString)
            val input = if (uri.scheme == "file") FileInputStream(File(requireNotNull(uri.path))) else context.contentResolver.openInputStream(uri)
            input?.use { BitmapFactory.decodeStream(it) }
        } catch (_: Exception) { null }
    }'''
if old_decode not in ps:
    raise SystemExit('Expected print adapter compatibility block not found')
printer.write_text(ps.replace(old_decode, new_decode))

# Version bump.
gradle = Path('rased-albarr/app/build.gradle')
gs = gradle.read_text()
if "versionCode 8" not in gs or "versionName '1.0.8'" not in gs:
    raise SystemExit('Unexpected base version')
gradle.write_text(gs.replace('versionCode 8', 'versionCode 11').replace("versionName '1.0.8'", "versionName '1.0.11'"))

# Fail build if any requested behavior was not applied.
check = main.read_text()
assert 'FrameLayout.LayoutParams(dp(56), dp(56), Gravity.LEFT or Gravity.TOP)' in check
assert 'marginEnd = dp(82)' in check
assert 'WindowInsets.Type.ime()' in check
assert 'requestRectangleOnScreen(rect, true)' in check
assert 'body.addView(locBox, fieldLp())' not in check
assert 'جارٍ تحديد الموقع عبر الشبكة وGPS...' in check
assert 'android:windowSoftInputMode="adjustResize"' in manifest.read_text()
print('v1.0.11 patch applied successfully')
