#!/usr/bin/env python3
"""
Direct APK Builder for PDF Spirit
Creates APK without complex build systems
"""

import os
import sys
import zipfile
import tempfile
from pathlib import Path
import shutil
import subprocess

def create_direct_apk():
    """Create APK directly using Python"""
    
    print("🔨 Building PDF Spirit APK Directly")
    print("===================================")
    print()
    
    # Check if we have required tools
    try:
        import PyPDF2
        print("✅ PyPDF2 found")
    except ImportError:
        print("📦 Installing PyPDF2...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyPDF2"], check=True)
        import PyPDF2
    
    # Create APK structure
    temp_dir = Path(tempfile.mkdtemp())
    apk_dir = temp_dir / "apk"
    apk_dir.mkdir()
    
    print(f"📁 Working in: {temp_dir}")
    
    # Create basic Android structure
    print("📋 Creating Android APK structure...")
    
    # Directories
    (apk_dir / "META-INF").mkdir()
    (apk_dir / "assets").mkdir()
    (apk_dir / "res" / "drawable").mkdir(parents=True)
    (apk_dir / "res" / "layout").mkdir(parents=True)
    (apk_dir / "res" / "values").mkdir(parents=True)
    (apk_dir / "lib" / "arm64-v8a").mkdir(parents=True)
    (apk_dir / "lib" / "armeabi-v7a").mkdir(parents=True)
    
    # AndroidManifest.xml
    manifest = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="org.pdfspirit.app"
    android:versionCode="1"
    android:versionName="1.0"
    android:installLocation="auto">
    
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    
    <uses-sdk android:minSdkVersion="21" android:targetSdkVersion="33" />
    
    <application
        android:label="PDF Spirit"
        android:icon="@drawable/icon"
        android:theme="@android:style/Theme.Material.Light">
        
        <activity
            android:name="org.kivy.android.PythonActivity"
            android:label="PDF Spirit"
            android:configChanges="keyboardHidden|orientation|screenSize"
            android:screenOrientation="portrait"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>'''
    
    with open(apk_dir / "AndroidManifest.xml", "w") as f:
        f.write(manifest)
    
    # strings.xml
    strings = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">PDF Spirit</string>
    <string name="private_version">1.0</string>
</resources>'''
    
    with open(apk_dir / "res" / "values" / "strings.xml", "w") as f:
        f.write(strings)
    
    # Simple icon
    icon_xml = '''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="48dp"
    android:height="48dp"
    android:viewportWidth="48"
    android:viewportHeight="48">
    <path
        android:fillColor="#4CAF50"
        android:pathData="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M8,12H16V14H8V12M8,16H13V18H8V16Z"/>
</vector>'''
    
    with open(apk_dir / "res" / "drawable" / "icon.xml", "w") as f:
        f.write(icon_xml)
    
    # Copy Python files to assets
    if Path("main.py").exists():
        shutil.copy("main.py", apk_dir / "assets" / "main.py")
        print("✅ Copied main.py")
    
    # Create a simple Python bootstrap
    bootstrap = '''#!/usr/bin/env python3
# PDF Spirit Android Bootstrap
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    # Import and run the main app
    from main import PDFSpiritApp
    PDFSpiritApp().run()
except ImportError:
    # Fallback simple interface
    print("PDF Spirit - Simple Mode")
    print("PDF processing functionality would go here")
    input("Press Enter to continue...")
'''
    
    with open(apk_dir / "assets" / "main.py", "w") as f:
        f.write(bootstrap)
    
    # Create MANIFEST.MF
    manifest_mf = '''Manifest-Version: 1.0
Created-By: PDF Spirit Direct Builder

'''
    
    with open(apk_dir / "META-INF" / "MANIFEST.MF", "w") as f:
        f.write(manifest_mf)
    
    # Create the APK
    print("📦 Creating APK file...")
    apk_path = Path("bin") / "pdfspirit-direct.apk"
    apk_path.parent.mkdir(exist_ok=True)
    
    with zipfile.ZipFile(apk_path, 'w', zipfile.ZIP_DEFLATED) as apk_zip:
        for root, dirs, files in os.walk(apk_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(apk_dir)
                apk_zip.write(file_path, arc_path)
    
    # Cleanup
    shutil.rmtree(temp_dir)
    
    print(f"✅ APK created: {apk_path}")
    print(f"📊 Size: {apk_path.stat().st_size:,} bytes")
    print()
    print("⚠️  Note: This is a basic APK structure.")
    print("   For full functionality, you'd need:")
    print("   - Python runtime for Android")
    print("   - Kivy framework compiled")
    print("   - Proper signing for installation")
    print()
    print("🎯 This demonstrates APK creation without GitHub!")
    print("   For a fully functional app, we'd need the complete build chain.")
    
    return apk_path

if __name__ == "__main__":
    create_direct_apk()
