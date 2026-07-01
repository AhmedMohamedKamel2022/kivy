[app]

title = Cyclic Resinline

package.name = CyclicResinline
package.domain = com.ahmed

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,json

version = 1.0

requirements = python3,kivy,requests,arabic-reshaper,python-bidi

orientation = portrait

fullscreen = 0

icon.filename = assets/icon.png

presplash.filename = assets/splash.png

android.permissions = INTERNET,ACCESS_NETWORK_STATE

android.api = 34
android.minapi = 24
android.sdk = 34
android.ndk = 25b

android.archs = arm64-v8a, armeabi-v7a

log_level = 2

android.accept_sdk_license = True

[buildozer]

warn_on_root = 1