from pathlib import Path

# Rebuild all verified fixes from v1.0.12 first.
exec(Path('rased-src/apply_v112.py').read_text(), globals())

printer = Path('rased-albarr/app/src/main/java/com/aboryan/rased/albarr/ObservationPrintAdapter.kt')
ps = printer.read_text()

old = '.setAlignment(Layout.Alignment.ALIGN_OPPOSITE)'
new = '.setAlignment(Layout.Alignment.ALIGN_NORMAL)'
if ps.count(old) != 1:
    raise SystemExit(f'Expected one print alignment target, found {ps.count(old)}')
ps = ps.replace(old, new)
printer.write_text(ps)

# v1.0.12 patch already advanced version metadata to 12; advance to 13.
gradle = Path('rased-albarr/app/build.gradle')
gs = gradle.read_text()
if "versionCode 12" not in gs or "versionName '1.0.12'" not in gs:
    raise SystemExit('Expected v1.0.12 version after compact UI patch')
gradle.write_text(gs.replace('versionCode 12', 'versionCode 13').replace("versionName '1.0.12'", "versionName '1.0.13'"))

check = printer.read_text()
assert '.setAlignment(Layout.Alignment.ALIGN_NORMAL)' in check
assert '.setTextDirection(TextDirectionHeuristics.RTL)' in check
assert '.setAlignment(Layout.Alignment.ALIGN_OPPOSITE)' not in check
print('v1.0.13 RTL print alignment applied to both single and grid printing')
