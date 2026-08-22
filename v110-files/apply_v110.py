from pathlib import Path
ROOT=Path("rased-albarr")

p=ROOT/'app/build.gradle'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("plugins {\n    id 'com.android.application'\n    id 'org.jetbrains.kotlin.android'\n}\n\nandroid {\n    namespace 'com.aboryan.rased.albarr'\n    compileSdk 35\n\n    defaultConfig {\n        applicationId 'com.aboryan.rased.albarr'\n        minSdk 24\n        targetSdk 35\n        versionCode 19\n        versionName '1.1.0'\n    }\n\n    buildTypes {\n        release {\n            minifyEnabled false\n            shrinkResources false\n        }\n    }\n\n    compileOptions {\n        sourceCompatibility JavaVersion.VERSION_17\n        targetCompatibility JavaVersion.VERSION_17\n    }\n    kotlinOptions {\n        jvmTarget = '17'\n    }\n}\n\n\ndependencies {\n    implementation 'com.google.zxing:core:3.5.3'\n    implementation 'androidx.core:core-location-altitude:1.0.0'\n}\n", encoding="utf-8")

p=ROOT/'app/src/main/AndroidManifest.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<?xml version="1.0" encoding="utf-8"?>\n<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n    <uses-permission android:name="android.permission.CAMERA" />\n    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />\n    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />\n    <uses-permission android:name="android.permission.INTERNET" />\n    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="28" />\n    <uses-feature android:name="android.hardware.camera.any" android:required="false" />\n    <uses-feature android:name="android.hardware.location.gps" android:required="false" />\n\n    <queries>\n        <intent><action android:name="android.media.action.IMAGE_CAPTURE" /></intent>\n        <intent><action android:name="android.intent.action.VIEW" /><data android:scheme="geo" /></intent>\n    </queries>\n\n    <application\n        android:allowBackup="true"\n        android:label="راصد البرية"\n        android:icon="@drawable/ic_launcher"\n        android:roundIcon="@drawable/ic_launcher"\n        android:supportsRtl="true"\n        android:theme="@android:style/Theme.Material.Light.NoActionBar">\n        <activity\n            android:name=".MainActivity"\n            android:screenOrientation="unspecified"\n            android:windowSoftInputMode="adjustResize"\n            android:exported="true">\n            <intent-filter>\n                <action android:name="android.intent.action.MAIN" />\n                <category android:name="android.intent.category.LAUNCHER" />\n            </intent-filter>\n        </activity>\n    </application>\n</manifest>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_add.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M19,13h-6v6h-2v-6H5v-2h6V5h2v6h6z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_arrow_back.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M20,11H7.83l5.59,-5.59L12,4l-8,8 8,8 1.41,-1.41L7.83,13H20z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_backup.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M19.35,10.04A7.49,7.49 0,0 0,5.5,8 5.994,5.994 0,0 0,6,20h13a5,5 0,0 0,0.35,-9.96zM13,13v4h-2v-4H8l4,-4 4,4h-3z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_camera.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M9,2L7.17,4H4c-1.1,0 -2,0.9 -2,2v12c0,1.1 0.9,2 2,2h16c1.1,0 2,-0.9 2,-2V6c0,-1.1 -0.9,-2 -2,-2h-3.17L15,2H9zM12,17a5,5 0,1 1,0,-10 5,5 0,0 1,0,10zM12,9a3,3 0,1 0,0,6 3,3 0,0 0,0,-6z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_chevron_down.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M7.41,8.59L12,13.17l4.59,-4.58L18,10l-6,6 -6,-6z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_chevron_left.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M15.41,7.41L14,6l-6,6 6,6 1.41,-1.41L10.83,12z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_chevron_up.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M7.41,15.41L12,10.83l4.59,4.58L18,14l-6,-6 -6,6z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_delete.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M6,19c0,1.1 0.9,2 2,2h8c1.1,0 2,-0.9 2,-2V7H6v12zM8,9h8v10H8zM15.5,4l-1,-1h-5l-1,1H5v2h14V4z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_edit.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M3,17.25V21h3.75L17.81,9.94l-3.75,-3.75L3,17.25zM20.71,7.04c0.39,-0.39 0.39,-1.03 0,-1.42l-2.34,-2.34a1.0,1.0 0,0 0,-1.42,0l-1.83,1.83 3.75,3.75z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_explore.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M12,2a10,10 0,1 0,0,20 10,10 0,0 0,0,-20zM14.7,9.3l-1.7,3.7 -3.7,1.7 1.7,-3.7z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_launcher.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">\n    <path android:fillColor="#F7F3EA" android:pathData="M0,0h108v108h-108z"/>\n    <path android:fillColor="#1F6348" android:pathData="M10,10h88a10,10 0,0 1,10 10v68a10,10 0,0 1,-10 10h-88a10,10 0,0 1,-10 -10v-68a10,10 0,0 1,10 -10z"/>\n    <path android:fillColor="#C48B48" android:pathData="M78,25a8,8 0,1 0,0.1 0z"/>\n    <path android:fillColor="#EFE2C7" android:pathData="M18,76L39,48l14,18 10,-13 27,23z"/>\n    <path android:fillColor="#B97845" android:pathData="M72,34c-9,0 -16,7 -16,16 0,12 16,27 16,27s16,-15 16,-27c0,-9 -7,-16 -16,-16z"/>\n    <path android:fillColor="#FFFFFF" android:pathData="M72,43a7,7 0,1 0,0.1 0z"/>\n</vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_location.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M12,2C8.13,2 5,5.13 5,9c0,5.25 7,13 7,13s7,-7.75 7,-13c0,-3.87 -3.13,-7 -7,-7zM12,11.5A2.5,2.5 0,1 1,12,6.5a2.5,2.5 0,0 1,0,5z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_photo.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M21,19V5c0,-1.1 -0.9,-2 -2,-2H5C3.9,3 3,3.9 3,5v14c0,1.1 0.9,2 2,2h14c1.1,0 2,-0.9 2,-2zM8.5,11.5l2.5,3.01L14.5,10l4.5,6H5z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_print.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M19,8H5c-1.66,0 -3,1.34 -3,3v4h4v4h12v-4h4v-4c0,-1.66 -1.34,-3 -3,-3zM16,17H8v-5h8v5zM18,3H6v4h12V3z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_restore.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M12,5V2L8,6l4,4V7c3.31,0 6,2.69 6,6s-2.69,6 -6,6 -6,-2.69 -6,-6H4c0,4.42 3.58,8 8,8s8,-3.58 8,-8 -3.58,-8 -8,-8z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_save.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M17,3H5c-1.1,0 -2,0.9 -2,2v14c0,1.1 0.9,2 2,2h14c1.1,0 2,-0.9 2,-2V7l-4,-4zM12,19a3,3 0,1 1,0,-6 3,3 0,0 1,0,6zM15,8H5V5h10v3z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_search.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M9.5,3a6.5,6.5 0,1 0,4.1 11.55L19.05,20 20.5,18.55l-5.45,-5.45A6.5,6.5 0,0 0,9.5,3zM9.5,5a4.5,4.5 0,1 1,0,9 4.5,4.5 0,0 1,0,-9z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_settings.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M19.14,12.94c0.04,-0.3 0.06,-0.61 0.06,-0.94s-0.02,-0.64 -0.07,-0.94l2.03,-1.58c0.18,-0.14 0.23,-0.41 0.12,-0.61l-1.92,-3.32c-0.12,-0.22 -0.37,-0.31 -0.6,-0.22l-2.39,0.96c-0.5,-0.38 -1.04,-0.7 -1.63,-0.94L14.38,2.81C14.35,2.57 14.14,2.4 13.9,2.4h-3.84c-0.24,0 -0.44,0.17 -0.48,0.41L9.22,5.35c-0.59,0.24 -1.13,0.57 -1.62,0.94l-2.39,-0.96c-0.22,-0.08 -0.47,0 -0.59,0.22L2.7,8.87c-0.12,0.21 -0.08,0.47 0.12,0.61l2.03,1.58c-0.05,0.3 -0.09,0.63 -0.09,0.94s0.03,0.64 0.08,0.94l-2.03,1.58c-0.18,0.14 -0.23,0.41 -0.12,0.61l1.92,3.32c0.12,0.22 0.37,0.31 0.6,0.22l2.39,-0.96c0.5,0.38 1.04,0.7 1.63,0.94l0.36,2.54c0.04,0.24 0.24,0.41 0.48,0.41h3.84c0.24,0 0.45,-0.17 0.48,-0.41l0.36,-2.54c0.59,-0.24 1.13,-0.56 1.63,-0.94l2.39,0.96c0.22,0.08 0.47,0 0.6,-0.22l1.92,-3.32c0.12,-0.22 0.07,-0.47 -0.12,-0.61zM12,15.6A3.6,3.6 0,1 1,12,8.4a3.6,3.6 0,0 1,0,7.2z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_share.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M18,16.08c-0.76,0 -1.44,0.3 -1.96,0.77L8.91,12.7c0.05,-0.23 0.09,-0.46 0.09,-0.7s-0.03,-0.47 -0.09,-0.7l7.05,-4.11A2.99,2.99 0,1 0,1 5c0,1.66 1.34,3 3,3 0.76,0 1.44,-0.3 1.96,-0.77l7.12,4.15c-0.05,0.2 -0.08,0.41 -0.08,0.62s0.03,0.42 0.08,0.62l-7.12,4.15A2.99,2.99 0,1 0,7 19c0,-0.24 -0.03,-0.47 -0.09,-0.7l7.13,-4.15c0.52,0.47 1.2,0.77 1.96,0.77a3,3 0,1 0,2,1.16z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_star.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M12,17.27L18.18,21l-1.64,-7.03L22,9.24l-7.19,-0.61L12,2 9.19,8.63 2,9.24l5.46,4.73L5.82,21z"/></vector>\n', encoding="utf-8")

p=ROOT/'app/src/main/res/drawable/ic_tune.xml'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text('<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FF000000" android:pathData="M3,17v2h6v-2H3zM3,5v2h10V5H3zM13,21v-2h8v-2h-8v-2h-2v6h2zM7,9v2H3v2h4v2h2V9H7zM21,13v-2H11v2h10zM15,9h2V7h4V5h-4V3h-2v6z"/></vector>\n', encoding="utf-8")

main = ROOT/"app/src/main/java/com/aboryan/rased/albarr/MainActivity.kt"
main.write_text("".join(Path(p).read_text(encoding="utf-8") for p in sorted(Path("v110-files").glob("MainActivity.kt.part*"))), encoding="utf-8")
printer = ROOT/"app/src/main/java/com/aboryan/rased/albarr/ObservationPrintAdapter.kt"
printer.write_text("".join(Path(p).read_text(encoding="utf-8") for p in sorted(Path("v110-files").glob("ObservationPrintAdapter.kt.part*"))), encoding="utf-8")
assert "versionCode 19" in (ROOT/"app/build.gradle").read_text()
assert "versionName '1.1.0'" in (ROOT/"app/build.gradle").read_text()
assert "الإصدار 1.1.0" in main.read_text()
assert "private val pageCount" in printer.read_text()
print("Rased AlBarr v1.1.0 visual identity applied")
