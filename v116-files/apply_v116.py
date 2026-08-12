from pathlib import Path

main = Path('rased-albarr/app/src/main/java/com/aboryan/rased/albarr/MainActivity.kt')
s = main.read_text()

def one(old, new, label):
    global s
    c = s.count(old)
    if c != 1:
        raise SystemExit(f'{label}: expected 1 target, found {c}')
    s = s.replace(old, new, 1)

old_meta = '''metaRow.addView(text("$loc  ·  ${date(item.createdAt)}", 13f, MUTED, true).apply { gravity = Gravity.RIGHT }, LinearLayout.LayoutParams(0, -2, 1f))'''
new_meta = '''val altitudeMeta = item.altitude?.let { "  ·  ↑ ${String.format(Locale.US, "%,.0f", it)} م" }.orEmpty()
        metaRow.addView(text("$loc$altitudeMeta  ·  ${date(item.createdAt)}", 13f, MUTED, true).apply { gravity = Gravity.RIGHT }, LinearLayout.LayoutParams(0, -2, 1f))'''
one(old_meta, new_meta, 'home altitude meta')

one('''        body.addView(infoBlock("الموقع", loc))
        val gpsDetails = gpsDetailsText(item)
''', '''        body.addView(infoBlock("الموقع", loc))
        item.altitude?.let {
            body.addView(infoBlock("الارتفاع عن سطح البحر", "${String.format(Locale.US, "%,.0f", it)} متر"))
        }
        val gpsDetails = gpsDetailsText(item)
''', 'detail altitude block')
one('''        item.altitude?.let { lines += "الارتفاع عن سطح البحر: ${it.toInt()} متر" }
''', '', 'remove duplicated gps altitude')

one('''wrap.addView(text("الإصدار 1.0.15   |   برمجة : ابوريان الغامدي", 12f, Color.rgb(150, 158, 154), true).apply { gravity = Gravity.CENTER; setPadding(0, dp(16), 0, 0) })''',
    '''wrap.addView(text("الإصدار 1.0.16   |   برمجة : ابوريان الغامدي", 12f, Color.rgb(150, 158, 154), true).apply { gravity = Gravity.CENTER; setPadding(0, dp(16), 0, 0) })''', 'settings version')
main.write_text(s)

printer = Path('rased-albarr/app/src/main/java/com/aboryan/rased/albarr/ObservationPrintAdapter.kt')
ps = printer.read_text()
old_print = 'item.altitude?.let { parts += "الارتفاع ${it.toInt()}م" }'
new_print = 'item.altitude?.let { parts += "الارتفاع عن سطح البحر ${String.format(Locale.US, "%,.0f", it)}م" }'
if ps.count(old_print) != 1:
    raise SystemExit(f'print altitude target: expected 1, found {ps.count(old_print)}')
ps = ps.replace(old_print, new_print, 1)
printer.write_text(ps)

gradle = Path('rased-albarr/app/build.gradle')
gs = gradle.read_text()
if 'versionCode 15' not in gs or "versionName '1.0.15'" not in gs:
    raise SystemExit('Expected v1.0.15 metadata')
gradle.write_text(gs.replace('versionCode 15', 'versionCode 16').replace("versionName '1.0.15'", "versionName '1.0.16'"))

check = main.read_text(); pcheck = printer.read_text()
assert 'الارتفاع عن سطح البحر' in check
assert 'الإصدار 1.0.16' in check
assert 'الارتفاع عن سطح البحر' in pcheck
assert 'versionCode 16' in gradle.read_text()
print('v1.0.16 altitude visibility patch applied')
