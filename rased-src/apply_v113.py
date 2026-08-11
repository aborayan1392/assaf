from pathlib import Path

# Start from the verified v1.0.11 source patch (keyboard + location + compatibility fixes).
exec(Path('rased-src/apply_v111.py').read_text(), globals())

main = Path('rased-albarr/app/src/main/java/com/aboryan/rased/albarr/MainActivity.kt')
s = main.read_text()

def one(old, new, label):
    global s
    c = s.count(old)
    if c != 1:
        raise SystemExit(f'{label}: expected 1 target, found {c}')
    s = s.replace(old, new)

# Reapply the verified v1.0.12 compact home UI using exact contextual targets.
one('val frame = FrameLayout(this).apply { setBackgroundColor(GREEN); minimumHeight = dp(150) }',
    'val frame = FrameLayout(this).apply { setBackgroundColor(GREEN); minimumHeight = dp(112) }', 'header height')
one('setPadding(dp(20), dp(18), dp(20), dp(18))',
    'setPadding(dp(18), dp(8), dp(18), dp(8))', 'header title padding')
one('titles.addView(text("راصد البرية", 28f, Color.WHITE, true).apply { gravity = Gravity.RIGHT })',
    'titles.addView(text("راصد البرية", 25f, Color.WHITE, true).apply { gravity = Gravity.RIGHT })', 'header title size')
one('''titles.addView(text("سجل ميداني للأشياء المميزة في رحلاتك", 16f, Color.rgb(232, 241, 236), true).apply {
            gravity = Gravity.RIGHT; setPadding(0, dp(10), 0, 0)
        })''',
    '''titles.addView(text("سجل ميداني للأشياء المميزة في رحلاتك", 15f, Color.rgb(232, 241, 236), true).apply {
            gravity = Gravity.RIGHT; setPadding(0, dp(3), 0, 0)
        })''', 'header subtitle')
one('frame.addView(titles, FrameLayout.LayoutParams(-1, -1).apply { marginEnd = dp(82) })',
    'frame.addView(titles, FrameLayout.LayoutParams(-1, -1).apply { marginEnd = dp(70) })', 'header settings clearance')
one('val settings = iconButton(R.drawable.ic_settings, Color.WHITE, 50).apply {',
    'val settings = iconButton(R.drawable.ic_settings, Color.WHITE, 40).apply {', 'settings icon size')
one('''frame.addView(settings, FrameLayout.LayoutParams(dp(56), dp(56), Gravity.LEFT or Gravity.TOP).apply {
            leftMargin = dp(20); topMargin = dp(20)
        })''',
    '''frame.addView(settings, FrameLayout.LayoutParams(dp(48), dp(48), Gravity.LEFT or Gravity.TOP).apply {
            leftMargin = dp(16); topMargin = dp(14)
        })''', 'settings button size')
one('''val toolsCard = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            background = rounded(Color.WHITE, 22f, strokeColor = Color.rgb(226, 224, 216))
            setPadding(dp(14), dp(8), dp(14), dp(8))
        }''',
    '''val toolsCard = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            background = rounded(Color.WHITE, 22f, strokeColor = Color.rgb(226, 224, 216))
            setPadding(dp(14), dp(4), dp(14), dp(4))
        }''', 'tools card padding')
one('val toolsLp = LinearLayout.LayoutParams(-1, -2).apply { setMargins(dp(16), dp(14), dp(16), dp(8)) }',
    'val toolsLp = LinearLayout.LayoutParams(-1, -2).apply { setMargins(dp(16), dp(8), dp(16), dp(4)) }', 'tools card margins')
one('''val toolsHeader = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            minimumHeight = dp(72)
            isClickable = true
            isFocusable = true
        }''',
    '''val toolsHeader = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            minimumHeight = dp(56)
            isClickable = true
            isFocusable = true
        }''', 'tools header height')
one('val filterIcon = iconView(R.drawable.ic_tune, TEAL, 44)', 'val filterIcon = iconView(R.drawable.ic_tune, TEAL, 34)', 'tools icon size')
one('toolsHeader.addView(filterIcon, LinearLayout.LayoutParams(dp(48), dp(48)))', 'toolsHeader.addView(filterIcon, LinearLayout.LayoutParams(dp(40), dp(40)))', 'tools icon box')
one('val toolsTitle = text("أدوات الرصد", 21f, INK, true).apply { gravity = Gravity.RIGHT or Gravity.CENTER_VERTICAL }',
    'val toolsTitle = text("أدوات الرصد", 19f, INK, true).apply { gravity = Gravity.RIGHT or Gravity.CENTER_VERTICAL }', 'tools title size')
one('val chevron = iconView(if (toolsExpanded) R.drawable.ic_chevron_up else R.drawable.ic_chevron_down, GREEN, 36)',
    'val chevron = iconView(if (toolsExpanded) R.drawable.ic_chevron_up else R.drawable.ic_chevron_down, GREEN, 28)', 'chevron size')
one('toolsHeader.addView(chevron, LinearLayout.LayoutParams(dp(48), dp(48)))', 'toolsHeader.addView(chevron, LinearLayout.LayoutParams(dp(40), dp(40)))', 'chevron box')
one('setPadding(dp(22), dp(10), dp(22), dp(8))', 'setPadding(dp(20), dp(6), dp(20), dp(4))', 'list heading padding')
one('listHead.addView(text("سجل الرصد", 23f, INK, true), LinearLayout.LayoutParams(0, -2, 1f))',
    'listHead.addView(text("سجل الرصد", 21f, INK, true), LinearLayout.LayoutParams(0, -2, 1f))', 'list heading size')
one('setPadding(0, dp(4), 0, dp(10))', 'setPadding(0, dp(2), 0, dp(6))', 'tools body padding')
if s.count('LinearLayout.LayoutParams(0, dp(86), 1f)') != 3:
    raise SystemExit('stats height: unexpected target count')
s = s.replace('LinearLayout.LayoutParams(0, dp(86), 1f)', 'LinearLayout.LayoutParams(0, dp(74), 1f)')
one('body.addView(add, LinearLayout.LayoutParams(-1, dp(62)).apply { setMargins(0, dp(12), 0, dp(10)) })',
    'body.addView(add, LinearLayout.LayoutParams(-1, dp(54)).apply { setMargins(0, dp(8), 0, dp(6)) })', 'add button compact')
one('body.addView(search, LinearLayout.LayoutParams(-1, dp(58)).apply { setMargins(0, 0, 0, dp(10)) })',
    'body.addView(search, LinearLayout.LayoutParams(-1, dp(52)).apply { setMargins(0, 0, 0, dp(6)) })', 'search compact')
one('filters.addView(spinner, LinearLayout.LayoutParams(0, dp(54), 1f).apply { marginEnd = dp(6) })',
    'filters.addView(spinner, LinearLayout.LayoutParams(0, dp(48), 1f).apply { marginEnd = dp(6) })', 'filter compact')
main.write_text(s)

# Fix Arabic alignment in the shared print text renderer.
# ALIGN_NORMAL + RTL aligns the natural paragraph edge to the RIGHT.
printer = Path('rased-albarr/app/src/main/java/com/aboryan/rased/albarr/ObservationPrintAdapter.kt')
ps = printer.read_text()
old_align = '.setAlignment(Layout.Alignment.ALIGN_OPPOSITE)'
if ps.count(old_align) != 1:
    raise SystemExit(f'Expected one print alignment target, found {ps.count(old_align)}')
ps = ps.replace(old_align, '.setAlignment(Layout.Alignment.ALIGN_NORMAL)')
printer.write_text(ps)

# Advance directly from v1.0.11 metadata to v1.0.13.
gradle = Path('rased-albarr/app/build.gradle')
gs = gradle.read_text()
if "versionCode 11" not in gs or "versionName '1.0.11'" not in gs:
    raise SystemExit('Expected v1.0.11 version after base patch')
gradle.write_text(gs.replace('versionCode 11', 'versionCode 13').replace("versionName '1.0.11'", "versionName '1.0.13'"))

check = main.read_text(); pcheck = printer.read_text()
assert 'minimumHeight = dp(112)' in check
assert 'minimumHeight = dp(56)' in check
assert 'WindowInsets.Type.ime()' in check
assert 'جارٍ تحديد الموقع عبر الشبكة وGPS...' in check
assert '.setAlignment(Layout.Alignment.ALIGN_NORMAL)' in pcheck
assert '.setTextDirection(TextDirectionHeuristics.RTL)' in pcheck
assert '.setAlignment(Layout.Alignment.ALIGN_OPPOSITE)' not in pcheck
print('v1.0.13 compact UI retained; RTL right alignment applied to single and collective printing')
