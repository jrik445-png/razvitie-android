[app]
title = Развитие
package.name = devassistant
package.domain = org.personal
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 0.1
requirements = python3==3.12.9,hostpython3==3.12.9,kivy==2.3.1
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.api = 33
android.minapi = 26
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

p4a.branch = master
