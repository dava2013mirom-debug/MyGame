[app]
title = Catch Circles
package.name = catchcircles
package.domain = org.mygame
source.dir = .
source.include_exts = py
version = 1.0
requirements = python3, pygame
orientation = portrait
fullscreen = 1

# Указываем использовать системный Android SDK
android.sdk_path = /usr/local/lib/android/sdk
android.build_tools = 33.0.0
android.archs = arm64-v8a, armeabi-v7a
android.api = 31
android.minapi = 21
android.accept_sdk_license = True