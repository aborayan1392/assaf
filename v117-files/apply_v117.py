from pathlib import Path

main = Path('rased-albarr/app/src/main/java/com/aboryan/rased/albarr/MainActivity.kt')
s = main.read_text()

def one(old, new, label):
    global s
    c = s.count(old)
    if c != 1:
        raise SystemExit(f'{label}: expected 1 target, found {c}')
    s = s.replace(old, new, 1)

one('LinearLayout.LayoutParams(-1, dp(150)).apply { setMargins(0, 0, 0, dp(12)) }',
    'LinearLayout.LayoutParams(-1, dp(132)).apply { setMargins(0, 0, 0, dp(9)) }', 'card height')
one('background = rounded(Color.WHITE, 20f, strokeColor = Color.rgb(228, 226, 218)); setPadding(dp(12), dp(12), dp(12), dp(12))',
    'background = rounded(Color.WHITE, 18f, strokeColor = Color.rgb(228, 226, 218)); setPadding(dp(9), dp(9), dp(9), dp(9))', 'card padding')
one('background = rounded(Color.rgb(241, 242, 238), 14f)',
    'background = rounded(Color.rgb(241, 242, 238), 12f)', 'image corner')
one('card.addView(image, LinearLayout.LayoutParams(dp(126), -1).apply { marginEnd = dp(14) })',
    'card.addView(image, LinearLayout.LayoutParams(dp(108), -1).apply { marginEnd = dp(11) })', 'image width')
one('titleRow.addView(text(item.title.ifBlank { "بدون عنوان" }, 19f, INK, true).apply { gravity = Gravity.RIGHT }, LinearLayout.LayoutParams(0, -2, 1f))',
    'titleRow.addView(text(item.title.ifBlank { "بدون عنوان" }, 18f, INK, true).apply { gravity = Gravity.RIGHT; maxLines = 1; ellipsize = android.text.TextUtils.TruncateAt.END }, LinearLayout.LayoutParams(0, -2, 1f))', 'title compact')
one('if (item.favorite) titleRow.addView(iconView(R.drawable.ic_star, GOLD, 26), LinearLayout.LayoutParams(dp(32), dp(32)))',
    'if (item.favorite) titleRow.addView(iconView(R.drawable.ic_star, GOLD, 23), LinearLayout.LayoutParams(dp(28), dp(28)))', 'favorite compact')
one('''texts.addView(text(chip, 14f, GREEN, true).apply {
            gravity = Gravity.RIGHT; background = rounded(Color.rgb(234, 246, 240), 14f); setPadding(dp(10), dp(5), dp(10), dp(5))
        }, LinearLayout.LayoutParams(-2, -2).apply { topMargin = dp(8) })''',
    '''texts.addView(text(chip, 13f, GREEN, true).apply {
            gravity = Gravity.RIGHT; background = rounded(Color.rgb(234, 246, 240), 13f); setPadding(dp(8), dp(3), dp(8), dp(3))
        }, LinearLayout.LayoutParams(-2, -2).apply { topMargin = dp(5) })''', 'chip compact')
one('val metaRow = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL; setPadding(0, dp(9), 0, 0) }',
    'val metaRow = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL; setPadding(0, dp(6), 0, 0) }', 'meta spacing')
one('metaRow.addView(iconView(R.drawable.ic_location, TEAL, 21), LinearLayout.LayoutParams(dp(24), dp(24)))',
    'metaRow.addView(iconView(R.drawable.ic_location, TEAL, 18), LinearLayout.LayoutParams(dp(21), dp(21)))', 'location compact')
one('metaRow.addView(text("$loc$altitudeMeta  ·  ${date(item.createdAt)}", 13f, MUTED, true).apply { gravity = Gravity.RIGHT }, LinearLayout.LayoutParams(0, -2, 1f))',
    'metaRow.addView(text("$loc$altitudeMeta  ·  ${date(item.createdAt)}", 12.5f, MUTED, true).apply { gravity = Gravity.RIGHT; maxLines = 1; ellipsize = android.text.TextUtils.TruncateAt.END }, LinearLayout.LayoutParams(0, -2, 1f))', 'meta compact')
one('card.addView(iconView(R.drawable.ic_chevron_left, Color.rgb(132, 151, 143), 28), LinearLayout.LayoutParams(dp(34), dp(34)))',
    'card.addView(iconView(R.drawable.ic_chevron_left, Color.rgb(132, 151, 143), 24), LinearLayout.LayoutParams(dp(28), dp(28)))', 'chevron compact')
one('wrap.addView(text("الإصدار 1.0.16   |   برمجة : ابوريان الغامدي", 12f, Color.rgb(150, 158, 154), true)',
    'wrap.addView(text("الإصدار 1.0.17   |   برمجة : ابوريان الغامدي", 12f, Color.rgb(150, 158, 154), true)', 'version footer')
main.write_text(s)

gradle = Path('rased-albarr/app/build.gradle')
gs = gradle.read_text()
if 'versionCode 16' not in gs or "versionName '1.0.16'" not in gs:
    raise SystemExit('Expected v1.0.16 metadata')
gradle.write_text(gs.replace('versionCode 16', 'versionCode 17').replace("versionName '1.0.16'", "versionName '1.0.17'"))

check = main.read_text()
assert 'dp(132)' in check
assert 'LinearLayout.LayoutParams(dp(108), -1)' in check
assert 'الإصدار 1.0.17' in check
assert 'versionCode 17' in gradle.read_text()
print('v1.0.17 compact observation cards applied')
