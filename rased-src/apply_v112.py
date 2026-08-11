from pathlib import Path

# Start from the verified v1.0.11 patch so location, SQLite, printing and keyboard behavior stay unchanged.
exec(Path('rased-src/apply_v111.py').read_text(), globals())

main = Path('rased-albarr/app/src/main/java/com/aboryan/rased/albarr/MainActivity.kt')
s = main.read_text()

def one(old, new, label):
    global s
    c = s.count(old)
    if c != 1:
        raise SystemExit(f'{label}: expected 1 target, found {c}')
    s = s.replace(old, new)

# Compact the home header without changing its structure or click behavior.
one('val frame = FrameLayout(this).apply { setBackgroundColor(GREEN); minimumHeight = dp(150) }',
    'val frame = FrameLayout(this).apply { setBackgroundColor(GREEN); minimumHeight = dp(112) }', 'header height')
one('setPadding(dp(20), dp(18), dp(20), dp(18))',
    'setPadding(dp(18), dp(8), dp(18), dp(8))', 'header title padding')
one('titles.addView(text("راصد البرية", 28f, Color.WHITE, true).apply { gravity = Gravity.RIGHT })',
    'titles.addView(text("راصد البرية", 25f, Color.WHITE, true).apply { gravity = Gravity.RIGHT })', 'header title size')
one('titles.addView(text("سجل ميداني للأشياء المميزة في رحلاتك", 16f, Color.rgb(232, 241, 236), true).apply {\n            gravity = Gravity.RIGHT; setPadding(0, dp(10), 0, 0)\n        })',
    'titles.addView(text("سجل ميداني للأشياء المميزة في رحلاتك", 15f, Color.rgb(232, 241, 236), true).apply {\n            gravity = Gravity.RIGHT; setPadding(0, dp(3), 0, 0)\n        })', 'header subtitle')
one('frame.addView(titles, FrameLayout.LayoutParams(-1, -1).apply { marginEnd = dp(82) })',
    'frame.addView(titles, FrameLayout.LayoutParams(-1, -1).apply { marginEnd = dp(70) })', 'header settings clearance')
one('val settings = iconButton(R.drawable.ic_settings, Color.WHITE, 50).apply {',
    'val settings = iconButton(R.drawable.ic_settings, Color.WHITE, 40).apply {', 'settings icon size')
one('frame.addView(settings, FrameLayout.LayoutParams(dp(56), dp(56), Gravity.LEFT or Gravity.TOP).apply {\n            leftMargin = dp(20); topMargin = dp(20)\n        })',
    'frame.addView(settings, FrameLayout.LayoutParams(dp(48), dp(48), Gravity.LEFT or Gravity.TOP).apply {\n            leftMargin = dp(16); topMargin = dp(14)\n        })', 'settings button size and margins')

# Compact collapsed tools card and surrounding whitespace.
one('setPadding(dp(14), dp(8), dp(14), dp(8))',
    'setPadding(dp(14), dp(4), dp(14), dp(4))', 'tools card padding')
one('val toolsLp = LinearLayout.LayoutParams(-1, -2).apply { setMargins(dp(16), dp(14), dp(16), dp(8)) }',
    'val toolsLp = LinearLayout.LayoutParams(-1, -2).apply { setMargins(dp(16), dp(8), dp(16), dp(4)) }', 'tools card margins')
one('minimumHeight = dp(72)', 'minimumHeight = dp(56)', 'tools header height')
one('val filterIcon = iconView(R.drawable.ic_tune, TEAL, 44)',
    'val filterIcon = iconView(R.drawable.ic_tune, TEAL, 34)', 'tools icon size')
one('toolsHeader.addView(filterIcon, LinearLayout.LayoutParams(dp(48), dp(48)))',
    'toolsHeader.addView(filterIcon, LinearLayout.LayoutParams(dp(40), dp(40)))', 'tools icon box')
one('val toolsTitle = text("أدوات الرصد", 21f, INK, true).apply { gravity = Gravity.RIGHT or Gravity.CENTER_VERTICAL }',
    'val toolsTitle = text("أدوات الرصد", 19f, INK, true).apply { gravity = Gravity.RIGHT or Gravity.CENTER_VERTICAL }', 'tools title size')
one('val chevron = iconView(if (toolsExpanded) R.drawable.ic_chevron_up else R.drawable.ic_chevron_down, GREEN, 36)',
    'val chevron = iconView(if (toolsExpanded) R.drawable.ic_chevron_up else R.drawable.ic_chevron_down, GREEN, 28)', 'chevron size')
one('toolsHeader.addView(chevron, LinearLayout.LayoutParams(dp(48), dp(48)))',
    'toolsHeader.addView(chevron, LinearLayout.LayoutParams(dp(40), dp(40)))', 'chevron box')

# Give the observation list more vertical room.
one('setPadding(dp(22), dp(10), dp(22), dp(8))',
    'setPadding(dp(20), dp(6), dp(20), dp(4))', 'list heading padding')
one('listHead.addView(text("سجل الرصد", 23f, INK, true), LinearLayout.LayoutParams(0, -2, 1f))',
    'listHead.addView(text("سجل الرصد", 21f, INK, true), LinearLayout.LayoutParams(0, -2, 1f))', 'list heading size')

# Moderate compaction when tools are expanded.
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

# v1.0.11 patch already changed the version from base 8 to 11; advance only the version metadata.
gradle = Path('rased-albarr/app/build.gradle')
gs = gradle.read_text()
if "versionCode 11" not in gs or "versionName '1.0.11'" not in gs:
    raise SystemExit('Expected v1.0.11 version after base patch')
gradle.write_text(gs.replace('versionCode 11', 'versionCode 12').replace("versionName '1.0.11'", "versionName '1.0.12'"))

check = main.read_text()
assert 'minimumHeight = dp(112)' in check
assert 'FrameLayout.LayoutParams(dp(48), dp(48), Gravity.LEFT or Gravity.TOP)' in check
assert 'minimumHeight = dp(56)' in check
assert 'text("أدوات الرصد", 19f' in check
assert 'WindowInsets.Type.ime()' in check
assert 'جارٍ تحديد الموقع عبر الشبكة وGPS...' in check
print('v1.0.12 compact UI patch applied successfully')
