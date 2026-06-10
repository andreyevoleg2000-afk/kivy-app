[app]
source.dir = .
title = AstroCalcMobile
package.name = mykivyapp
package.domain = org.test
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy

# Обязательные системные настройки для Android
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk_api = 21
android.permissions = INTERNET
android.archs = arm64-v8a
android.accept_sdk_license = True
android.release_artifact = apk

[buildozer]
log_level = 2
