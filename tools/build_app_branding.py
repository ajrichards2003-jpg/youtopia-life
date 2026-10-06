from pathlib import Path
from PIL import Image,ImageDraw
import json
ROOT=Path(__file__).resolve().parents[1]
for mobile,web in [('mobile','app'),('mobile-ascent','ascent-app')]:
 icon=Image.open(ROOT/web/'icon-1024.png').convert('RGB')
 ios=ROOT/mobile/'ios/App/App/Assets.xcassets'
 icon.save(ios/'AppIcon.appiconset/AppIcon-512@2x.png')
 def splash(w,h):
  im=Image.new('RGB',(w,h),(7,23,19));mark=icon.resize((round(min(w,h)*.30),)*2,Image.Resampling.LANCZOS);im.paste(mark,((w-mark.width)//2,(h-mark.height)//2));return im
 for p in (ios/'Splash.imageset').glob('*.png'):splash(2732,2732).save(p)
 res=ROOT/mobile/'android/app/src/main/res'
 for density,size,foreground in [('mdpi',48,108),('hdpi',72,162),('xhdpi',96,216),('xxhdpi',144,324),('xxxhdpi',192,432)]:
  out=res/('mipmap-'+density)
  for name in ['ic_launcher.png','ic_launcher_round.png']:icon.resize((size,size),Image.Resampling.LANCZOS).save(out/name)
  icon.resize((foreground,foreground),Image.Resampling.LANCZOS).save(out/'ic_launcher_foreground.png')
 # The adaptive icon no longer points to the Capacitor template foreground.
 for p in (res/'mipmap-anydpi-v26').glob('*.xml'):
  p.write_text('<?xml version="1.0" encoding="utf-8"?><adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/ic_launcher_background"/><foreground android:drawable="@mipmap/ic_launcher_foreground"/></adaptive-icon>\n')
 (res/'values/ic_launcher_background.xml').write_text('<?xml version="1.0" encoding="utf-8"?><resources><color name="ic_launcher_background">#071713</color></resources>\n')
 for p in res.glob('drawable*/splash.png'):
  old=Image.open(p);splash(*old.size).save(p)
 # Android 12+ splash API uses the branded launcher, retaining the launch theme.
 p=res/'values/styles.xml';s=p.read_text();s=s if 'windowSplashScreenBackground' in s else s.replace('<item name="android:background">@drawable/splash</item>','<item name="android:background">@drawable/splash</item>\n        <item name="windowSplashScreenBackground">#071713</item>\n        <item name="windowSplashScreenAnimatedIcon">@mipmap/ic_launcher</item>\n        <item name="postSplashScreenTheme">@style/AppTheme.NoActionBar</item>');p.write_text(s)
 print(mobile,'branded icons and launch assets generated')
