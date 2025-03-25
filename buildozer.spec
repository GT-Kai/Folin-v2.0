buildozer init
[app]
title = 茯苓语音助手
package.name = fulingapp
package.domain = org.fuling
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
   
requirements = python3,kivy,numpy,pyaudio
   
android.permissions = INTERNET,RECORD_AUDIO,WAKE_LOCK
android.api = 29
android.minapi = 21
android.ndk = 21e