from pathlib import Path
import re

main = Path('rased-albarr/app/src/main/java/com/aboryan/rased/albarr/MainActivity.kt')
s = main.read_text()

def one(old, new, label):
    global s
    c = s.count(old)
    if c != 1:
        raise SystemExit(f'{label}: expected 1 target, found {c}')
    s = s.replace(old, new, 1)

one(
'''        private val RED = Color.rgb(176, 68, 61)
    }''',
'''        private val RED = Color.rgb(176, 68, 61)
        private const val UI_SCALE = 0.94f
    }''',
'ui scale constant')

one(
'''    private lateinit var appTypeface: Typeface
    private var currentScreen = "home"''',
'''    private lateinit var appTypeface: Typeface
    private var cairoSelected = false
    private var currentScreen = "home"''',
'font state')

old_font = '''    private fun loadTypeface(): Typeface = try {
        // ندعم Cairo إذا كان مضمنًا، وإلا نستخدم خط النظام العربي بدل السقوط إلى Bold ثقيل.
        val base = Typeface.createFromAsset(assets, "fonts/Cairo.ttf")
        if (Build.VERSION.SDK_INT >= 28) Typeface.create(base, 500, false) else Typeface.create(base, Typeface.NORMAL)
    } catch (_: Exception) {
        Typeface.create("sans-serif", Typeface.NORMAL)
    }
'''
new_font = '''    private fun loadTypeface(): Typeface {
        val choice = getSharedPreferences("rased_prefs", MODE_PRIVATE).getString("font_choice", "system") ?: "system"
        cairoSelected = choice == "cairo"
        if (!cairoSelected) return Typeface.create("sans-serif", Typeface.NORMAL)
        return try {
            val base = Typeface.createFromAsset(assets, "fonts/Cairo.ttf")
            if (Build.VERSION.SDK_INT >= 28) Typeface.create(base, 400, false) else Typeface.create(base, Typeface.NORMAL)
        } catch (_: Exception) {
            cairoSelected = false
            Typeface.create("sans-serif", Typeface.NORMAL)
        }
    }

    private fun styledTypeface(bold: Boolean): Typeface {
        if (!bold) return appTypeface
        return if (cairoSelected && Build.VERSION.SDK_INT >= 28) {
            Typeface.create(appTypeface, 600, false)
        } else {
            Typeface.create(appTypeface, Typeface.BOLD)
        }
    }
'''
one(old_font, new_font, 'load typeface')

anchor = '''        wrap.addView(settingsRow(R.drawable.ic_delete, "مسح كل البيانات", "حذف جميع الأرصاد نهائيًا", RED) {
            dialog.dismiss(); confirmClearAll()
        })'''
replacement = '''        val currentFontLabel = if (getSharedPreferences("rased_prefs", MODE_PRIVATE).getString("font_choice", "system") == "cairo") "Cairo" else "الخط الافتراضي للنظام"
        wrap.addView(settingsRow(R.drawable.ic_tune, "خط التطبيق", "الخط الحالي: $currentFontLabel — اضغط للتغيير", TEAL) {
            dialog.dismiss(); showFontDialog()
        })
        wrap.addView(settingsRow(R.drawable.ic_delete, "مسح كل البيانات", "حذف جميع الأرصاد نهائيًا", RED) {
            dialog.dismiss(); confirmClearAll()
        })'''
one(anchor, replacement, 'settings font row')

one(
'''    private fun settingsRow(icon: Int, title: String, subtitle: String, color: Int, action: () -> Unit): View {''',
'''    private fun showFontDialog() {
        val prefs = getSharedPreferences("rased_prefs", MODE_PRIVATE)
        val current = prefs.getString("font_choice", "system") ?: "system"
        val options = arrayOf("الخط الافتراضي للنظام", "Cairo")
        val checked = if (current == "cairo") 1 else 0
        AlertDialog.Builder(this)
            .setTitle("اختيار خط التطبيق")
            .setSingleChoiceItems(options, checked) { dialog, which ->
                val value = if (which == 1) "cairo" else "system"
                prefs.edit().putString("font_choice", value).apply()
                dialog.dismiss()
                recreate()
            }
            .setNegativeButton("إلغاء", null)
            .show()
    }

    private fun settingsRow(icon: Int, title: String, subtitle: String, color: Int, action: () -> Unit): View {''',
'font dialog')

one(
'''wrap.addView(text("الإصدار 1.1.0   |   برمجة : ابوريان الغامدي", 12f, Color.rgb(150, 158, 154), true)''',
'''wrap.addView(text("الإصدار 1.1.1   |   برمجة : ابوريان الغامدي", 12f, Color.rgb(150, 158, 154), true)''',
'version footer')

# Scale direct text-size assignments used by EditText/Spinner/Button/CheckBox while text() is handled separately below.
s = re.sub(r'textSize = (\d+(?:\.\d+)?f)(?!\s*\*\s*UI_SCALE)', r'textSize = \1 * UI_SCALE', s)

one(
'''        text = s; textSize = sp; setTextColor(color); typeface = if (bold) Typeface.create(appTypeface, Typeface.BOLD) else appTypeface; includeFontPadding = false''',
'''        text = s; textSize = sp * UI_SCALE; setTextColor(color); typeface = styledTypeface(bold); includeFontPadding = false''',
'text helper')

one(
'''    private fun dp(v: Int): Int = (v * resources.displayMetrics.density + .5f).toInt()
    private fun dp(v: Float): Int = (v * resources.displayMetrics.density + .5f).toInt()''',
'''    private fun dp(v: Int): Int = (v * resources.displayMetrics.density * UI_SCALE + .5f).toInt()
    private fun dp(v: Float): Int = (v * resources.displayMetrics.density * UI_SCALE + .5f).toInt()''',
'dp scale')

main.write_text(s)

gradle = Path('rased-albarr/app/build.gradle')
gs = gradle.read_text()
if 'versionCode 19' not in gs or "versionName '1.1.0'" not in gs:
    raise SystemExit('Expected v1.1.0 metadata before v1.1.1 patch')
gs = gs.replace('versionCode 19', 'versionCode 20').replace("versionName '1.1.0'", "versionName '1.1.1'")
gradle.write_text(gs)

check = main.read_text()
assert 'private const val UI_SCALE = 0.94f' in check
assert 'font_choice' in check
assert 'Typeface.create(base, 400, false)' in check
assert 'Typeface.create(appTypeface, 600, false)' in check
assert 'showFontDialog()' in check
assert 'الإصدار 1.1.1' in check
assert 'textSize = sp * UI_SCALE' in check
assert 'versionCode 20' in gradle.read_text()
assert "versionName '1.1.1'" in gradle.read_text()
print('v1.1.1 font selector and compact UI applied')
