from pathlib import Path
src = Path('rased-src/apply_v112.py').read_text()
old = "one('minimumHeight = dp(72)', 'minimumHeight = dp(56)', 'tools header height')"
new = '''tools_old = """val toolsHeader = LinearLayout(this).apply {\n            orientation = LinearLayout.HORIZONTAL\n            gravity = Gravity.CENTER_VERTICAL\n            minimumHeight = dp(72)"""\ntools_new = """val toolsHeader = LinearLayout(this).apply {\n            orientation = LinearLayout.HORIZONTAL\n            gravity = Gravity.CENTER_VERTICAL\n            minimumHeight = dp(56)"""\none(tools_old, tools_new, 'tools header height')'''
if old not in src:
    raise SystemExit('v1.0.12 tools header patch source not found')
src = src.replace(old, new)
exec(compile(src, 'apply_v112_fixed_runtime.py', 'exec'), globals())
