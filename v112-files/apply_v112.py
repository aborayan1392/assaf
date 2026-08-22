from pathlib import Path

main = Path('rased-albarr/app/src/main/java/com/aboryan/rased/albarr/MainActivity.kt')
s = main.read_text()

def one(old, new, label):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 target, found {count}')
    s = s.replace(old, new, 1)

one(
'''import android.Manifest\n''',
'''import android.Manifest\nimport android.animation.Animator\nimport android.animation.ValueAnimator\n''',
'animation imports')

one(
'''import android.view.WindowInsets\n''',
'''import android.view.WindowInsets\nimport android.view.animation.DecelerateInterpolator\n''',
'interpolator import')

one(
'''    private var toolsExpanded = false\n    private var searchQuery = ""''',
'''    private var toolsExpanded = false\n    private var homeTopCollapsed = false\n    private var homeTopAnimator: ValueAnimator? = null\n    private var searchQuery = ""''',
'folding state')

old_top = '''        val root = rootLayout()\n        root.addView(homeHeader())\n\n        val actions = buildPrimaryActions()\n        root.addView(actions, LinearLayout.LayoutParams(-1, dp(54)).apply {\n            setMargins(dp(16), dp(10), dp(16), dp(8))\n        })\n\n        val search = buildSearchField()\n        root.addView(search, LinearLayout.LayoutParams(-1, dp(50)).apply {\n            setMargins(dp(16), 0, dp(16), dp(8))\n        })\n\n        val toolsCard = LinearLayout(this).apply {\n            orientation = LinearLayout.VERTICAL\n            background = rounded(CARD, 18f, strokeColor = LINE)\n            setPadding(dp(12), dp(2), dp(12), dp(2))\n            elevation = dp(1).toFloat()\n        }\n        root.addView(toolsCard, LinearLayout.LayoutParams(-1, -2).apply {\n            setMargins(dp(16), 0, dp(16), dp(7))\n        })'''
new_top = '''        val root = rootLayout()\n        homeTopCollapsed = getSharedPreferences("rased_prefs", MODE_PRIVATE).getBoolean("home_top_collapsed", false)\n\n        val topPanel = LinearLayout(this).apply {\n            orientation = LinearLayout.VERTICAL\n        }\n        topPanel.addView(homeHeader())\n\n        val actions = buildPrimaryActions()\n        topPanel.addView(actions, LinearLayout.LayoutParams(-1, dp(54)).apply {\n            setMargins(dp(16), dp(10), dp(16), dp(8))\n        })\n\n        val search = buildSearchField()\n        topPanel.addView(search, LinearLayout.LayoutParams(-1, dp(50)).apply {\n            setMargins(dp(16), 0, dp(16), dp(8))\n        })\n\n        val toolsCard = LinearLayout(this).apply {\n            orientation = LinearLayout.VERTICAL\n            background = rounded(CARD, 18f, strokeColor = LINE)\n            setPadding(dp(12), dp(2), dp(12), dp(2))\n            elevation = dp(1).toFloat()\n        }\n        topPanel.addView(toolsCard, LinearLayout.LayoutParams(-1, -2).apply {\n            setMargins(dp(16), 0, dp(16), dp(7))\n        })\n        root.addView(topPanel, LinearLayout.LayoutParams(-1, -2))\n        if (homeTopCollapsed) topPanel.visibility = View.GONE'''
one(old_top, new_top, 'wrap top panel')

old_list_head = '''        listHead.addView(text("الأرصاد الأخيرة", 20f, INK, true), LinearLayout.LayoutParams(0, -2, 1f))\n        countLabel = metaChip("", MIST, GREEN, 12.5f).apply { gravity = Gravity.CENTER }\n        listHead.addView(countLabel, LinearLayout.LayoutParams(-2, dp(31)))\n        root.addView(listHead)'''
new_list_head = '''        listHead.addView(text("الأرصاد الأخيرة", 20f, INK, true), LinearLayout.LayoutParams(0, -2, 1f))\n\n        countLabel = metaChip("", MIST, GREEN, 12.5f).apply { gravity = Gravity.CENTER }\n        listHead.addView(countLabel, LinearLayout.LayoutParams(-2, dp(31)).apply { marginStart = dp(6) })\n\n        val foldToggle = homeFoldToggle(homeTopCollapsed)\n        foldToggle.setOnClickListener {\n            animateHomeTop(topPanel, !homeTopCollapsed, foldToggle)\n        }\n        listHead.addView(foldToggle, LinearLayout.LayoutParams(-2, dp(32)))\n        root.addView(listHead)'''
one(old_list_head, new_list_head, 'list fold toggle')

helper_anchor = '''    private fun buildToolsBody(): LinearLayout {'''
helpers = '''    private fun homeFoldToggle(collapsed: Boolean): TextView = TextView(this).apply {\n        gravity = Gravity.CENTER\n        setTextColor(GREEN_DARK)\n        typeface = styledTypeface(true)\n        textSize = 11.8f * UI_SCALE\n        background = rounded(Color.rgb(238, 246, 241), 14f, strokeColor = Color.rgb(205, 222, 212))\n        setPadding(dp(9), 0, dp(9), 0)\n        minimumHeight = dp(30)\n        updateHomeFoldToggle(this, collapsed)\n    }\n\n    private fun updateHomeFoldToggle(toggle: TextView, collapsed: Boolean) {\n        toggle.text = if (collapsed) "إظهار الأعلى" else "طي الأعلى"\n        toggle.contentDescription = if (collapsed) "إظهار الجزء العلوي" else "طي الجزء العلوي"\n        val drawable = getDrawable(if (collapsed) R.drawable.ic_chevron_down else R.drawable.ic_chevron_up)?.mutate()\n        drawable?.setTint(GREEN)\n        drawable?.setBounds(0, 0, dp(17), dp(17))\n        toggle.setCompoundDrawablesRelative(drawable, null, null, null)\n        toggle.compoundDrawablePadding = dp(3)\n    }\n\n    private fun animateHomeTop(panel: View, collapse: Boolean, toggle: TextView) {\n        homeTopAnimator?.cancel()\n        toggle.isEnabled = false\n        val prefs = getSharedPreferences("rased_prefs", MODE_PRIVATE)\n\n        if (collapse) {\n            val startHeight = panel.height\n            if (startHeight <= 0) {\n                panel.visibility = View.GONE\n                homeTopCollapsed = true\n                prefs.edit().putBoolean("home_top_collapsed", true).apply()\n                updateHomeFoldToggle(toggle, true)\n                toggle.isEnabled = true\n                return\n            }\n\n            var cancelled = false\n            val animator = ValueAnimator.ofInt(startHeight, 0).apply {\n                duration = 240L\n                interpolator = DecelerateInterpolator(1.35f)\n                addUpdateListener { valueAnimator ->\n                    val fraction = valueAnimator.animatedFraction\n                    panel.layoutParams.height = valueAnimator.animatedValue as Int\n                    panel.alpha = 1f - (0.22f * fraction)\n                    panel.translationY = -dp(10).toFloat() * fraction\n                    panel.requestLayout()\n                }\n                addListener(object : Animator.AnimatorListener {\n                    override fun onAnimationStart(animation: Animator) = Unit\n                    override fun onAnimationRepeat(animation: Animator) = Unit\n                    override fun onAnimationCancel(animation: Animator) {\n                        cancelled = true\n                        toggle.isEnabled = true\n                    }\n                    override fun onAnimationEnd(animation: Animator) {\n                        if (cancelled) return\n                        panel.visibility = View.GONE\n                        panel.layoutParams.height = ViewGroup.LayoutParams.WRAP_CONTENT\n                        panel.alpha = 1f\n                        panel.translationY = 0f\n                        homeTopCollapsed = true\n                        prefs.edit().putBoolean("home_top_collapsed", true).apply()\n                        updateHomeFoldToggle(toggle, true)\n                        toggle.isEnabled = true\n                        homeTopAnimator = null\n                    }\n                })\n            }\n            homeTopAnimator = animator\n            animator.start()\n        } else {\n            panel.visibility = View.VISIBLE\n            panel.layoutParams.height = ViewGroup.LayoutParams.WRAP_CONTENT\n            val parentWidth = (panel.parent as? View)?.width?.takeIf { it > 0 } ?: resources.displayMetrics.widthPixels\n            panel.measure(\n                View.MeasureSpec.makeMeasureSpec(parentWidth, View.MeasureSpec.EXACTLY),\n                View.MeasureSpec.makeMeasureSpec(0, View.MeasureSpec.UNSPECIFIED)\n            )\n            val targetHeight = panel.measuredHeight\n            if (targetHeight <= 0) {\n                panel.layoutParams.height = ViewGroup.LayoutParams.WRAP_CONTENT\n                panel.alpha = 1f\n                panel.translationY = 0f\n                homeTopCollapsed = false\n                prefs.edit().putBoolean("home_top_collapsed", false).apply()\n                updateHomeFoldToggle(toggle, false)\n                toggle.isEnabled = true\n                return\n            }\n\n            panel.layoutParams.height = 0\n            panel.alpha = 0.78f\n            panel.translationY = -dp(8).toFloat()\n            panel.requestLayout()\n\n            var cancelled = false\n            val animator = ValueAnimator.ofInt(0, targetHeight).apply {\n                duration = 280L\n                interpolator = DecelerateInterpolator(1.25f)\n                addUpdateListener { valueAnimator ->\n                    val fraction = valueAnimator.animatedFraction\n                    panel.layoutParams.height = valueAnimator.animatedValue as Int\n                    panel.alpha = 0.78f + (0.22f * fraction)\n                    panel.translationY = -dp(8).toFloat() * (1f - fraction)\n                    panel.requestLayout()\n                }\n                addListener(object : Animator.AnimatorListener {\n                    override fun onAnimationStart(animation: Animator) = Unit\n                    override fun onAnimationRepeat(animation: Animator) = Unit\n                    override fun onAnimationCancel(animation: Animator) {\n                        cancelled = true\n                        toggle.isEnabled = true\n                    }\n                    override fun onAnimationEnd(animation: Animator) {\n                        if (cancelled) return\n                        panel.layoutParams.height = ViewGroup.LayoutParams.WRAP_CONTENT\n                        panel.alpha = 1f\n                        panel.translationY = 0f\n                        homeTopCollapsed = false\n                        prefs.edit().putBoolean("home_top_collapsed", false).apply()\n                        updateHomeFoldToggle(toggle, false)\n                        toggle.isEnabled = true\n                        homeTopAnimator = null\n                    }\n                })\n            }\n            homeTopAnimator = animator\n            animator.start()\n        }\n    }\n\n    private fun buildToolsBody(): LinearLayout {'''
one(helper_anchor, helpers, 'folding helpers')

one(
'''wrap.addView(text("الإصدار 1.1.1   |   برمجة : ابوريان الغامدي", 12f, Color.rgb(150, 158, 154), true)''',
'''wrap.addView(text("الإصدار 1.1.2   |   برمجة : ابوريان الغامدي", 12f, Color.rgb(150, 158, 154), true)''',
'version footer')

main.write_text(s)

gradle = Path('rased-albarr/app/build.gradle')
gs = gradle.read_text()
if 'versionCode 20' not in gs or "versionName '1.1.1'" not in gs:
    raise SystemExit('Expected v1.1.1 metadata before v1.1.2 patch')
gs = gs.replace('versionCode 20', 'versionCode 21').replace("versionName '1.1.1'", "versionName '1.1.2'")
gradle.write_text(gs)

changes = Path('rased-albarr/CHANGES_1.1.2_AR.md')
changes.write_text('''# راصد البرية v1.1.2\n\n- إضافة طي احترافي للجزء العلوي من الشاشة الرئيسية.\n- زر الطي مدمج في صف «الأرصاد الأخيرة» حتى لا يستهلك مساحة إضافية.\n- حركة انكماش وفتح سلسة مع تلاشي خفيف.\n- حفظ حالة الطي تلقائيًا عند التنقل والعودة.\n- الإبقاء على خط النظام/Cairo وخيار الواجهة المصغرة من v1.1.1.\n- قاعدة البيانات والحفظ والاستيراد والتصدير دون تغيير.\n''')

check = main.read_text()
assert 'home_top_collapsed' in check
assert 'animateHomeTop' in check
assert 'إظهار الأعلى' in check
assert 'طي الأعلى' in check
assert 'ValueAnimator.ofInt' in check
assert 'الإصدار 1.1.2' in check
assert 'versionCode 21' in gradle.read_text()
assert "versionName '1.1.2'" in gradle.read_text()
print('v1.1.2 professional folding header applied')
