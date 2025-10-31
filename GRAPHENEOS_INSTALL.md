# 📱 PDF Spirit - GrapheneOS Installation Guide

**Native Android PDF label processing for privacy-focused users**

## 🔒 Why Perfect for GrapheneOS

PDF Spirit is **designed for privacy** - exactly what GrapheneOS users want:
- ✅ **No internet permissions** - Cannot connect to network
- ✅ **No tracking or analytics** - Zero data collection
- ✅ **Open source code** - Full transparency
- ✅ **Local processing only** - Files never leave device
- ✅ **Minimal permissions** - Only storage access needed

## 📱 Installation on GrapheneOS

### Step 1: Get the APK
**Option A - Pre-built APK:**
- Get `pdfspirit-1.0-debug.apk` from your friend
- Copy to your phone via USB, cloud, or direct download

**Option B - Build yourself:**
- Follow `SUPER_SIMPLE_GITHUB.md` to build your own
- Complete control over the build process

### Step 2: Enable Installation
1. **Settings** → **Apps** → **Special app access**
2. **Install unknown apps**
3. **Select your file manager** (Files, etc.)
4. **Toggle "Allow from this source"** → **ON**

### Step 3: Install PDF Spirit
1. **Open file manager** → **Navigate to APK location**
2. **Tap the APK file** → **Install**
3. **Review permissions** (only storage access)
4. **Tap "Install"** → **Done!**

### Step 4: Grant Permissions
1. **Open PDF Spirit** for first time
2. **Grant storage permission** when prompted
3. **Allow access to files** → **Yes**

## 🎯 Using PDF Spirit on GrapheneOS

### First Launch:
1. **Find "PDF Spirit"** in app drawer
2. **Tap to open** → Clean, simple interface
3. **Tap "Scan for PDFs"** → Finds files in Downloads
4. **See your PDFs listed** with file sizes

### Processing PDFs:
1. **Download PostNord PDF** to your phone
2. **Open PDF Spirit** → **Tap "Scan for PDFs"**
3. **Tap "Process"** next to desired PDF
4. **Watch progress bar** → **Success notification**
5. **Find result** in Documents/PDFSpirit folder

### File Management:
- **Input:** Downloads folder (where you save PDFs)
- **Output:** Documents/PDFSpirit folder
- **Access:** Use any file manager to view results
- **Sharing:** Share processed PDFs directly from Documents

## 🔧 GrapheneOS Specific Features

### Privacy Protections:
- **Network isolation** - App cannot access internet
- **Sandboxed operation** - Isolated from other apps
- **Permission control** - You control what it accesses
- **No background activity** - Only runs when you use it

### Security Benefits:
- **Minimal attack surface** - Simple, focused functionality
- **No external dependencies** - Self-contained processing
- **Auditable code** - Open source for review
- **Local execution** - No cloud or server dependencies

## 🛡️ GrapheneOS Compatibility

### Tested On:
- **GrapheneOS latest** - Full compatibility
- **Android 10+** - All modern GrapheneOS versions
- **Pixel devices** - Primary GrapheneOS hardware
- **ARM64 architecture** - Standard GrapheneOS setup

### Performance:
- **Fast processing** - Optimized for mobile
- **Low resource usage** - Minimal battery impact
- **Smooth UI** - Native Android experience
- **Quick startup** - Ready to use instantly

## 🔍 Verifying the App

### Security Checks:
```bash
# Check APK permissions (if you have ADB)
aapt dump permissions pdfspirit-1.0-debug.apk

# Should only show:
# - READ_EXTERNAL_STORAGE
# - WRITE_EXTERNAL_STORAGE
```

### What to Look For:
- ✅ **Only storage permissions** - No network, camera, etc.
- ✅ **No background services** - Runs only when opened
- ✅ **No internet access** - Cannot connect to network
- ✅ **Clean manifest** - No suspicious permissions

## 🎨 GrapheneOS User Experience

### Interface Design:
- **Material Design** - Familiar Android look
- **Touch optimized** - Perfect for phone use
- **Clear feedback** - Progress bars and notifications
- **Simple navigation** - Easy to understand

### Workflow Integration:
- **Downloads integration** - Finds PDFs automatically
- **File manager friendly** - Works with any file app
- **Share menu support** - Easy sharing of results
- **Print integration** - Direct printing from Documents

## 🆘 GrapheneOS Troubleshooting

### App Won't Install:
- **Check "Unknown apps" setting** - Must be enabled
- **Verify APK integrity** - Re-download if corrupted
- **Free up space** - Need 50MB+ available
- **Restart phone** - Sometimes helps with installation

### No Permissions Granted:
- **Settings** → **Apps** → **PDF Spirit** → **Permissions**
- **Enable "Storage"** → **Allow**
- **Restart app** after changing permissions

### Can't Find PDFs:
- **Check Downloads folder** - PDFs must be there
- **Verify file names** - Must end in .pdf
- **Refresh app** - Close and reopen PDF Spirit
- **Check file permissions** - Files must be readable

## 🎉 Perfect GrapheneOS Solution

**PDF Spirit gives GrapheneOS users:**
- **Native mobile PDF processing** - No desktop needed
- **Complete privacy protection** - Zero data leakage
- **Professional results** - Perfect label cropping
- **Offline operation** - No internet dependencies
- **Open source transparency** - Auditable code

## 🎯 Why GrapheneOS Users Love It

**Privacy First:**
- No tracking, no analytics, no data collection
- Local processing only - files never leave device
- Minimal permissions - only what's absolutely needed

**Security Focused:**
- No network access - cannot connect to internet
- Sandboxed operation - isolated from other apps
- Open source code - can be reviewed and modified

**User Controlled:**
- You decide what to process
- You control when it runs
- You own your data completely

---

## 🔒 Bottom Line for GrapheneOS

**PDF Spirit is the perfect PDF solution for privacy-conscious GrapheneOS users who refuse to compromise on security or functionality.**

**Your PostNord labels will be perfectly cropped while your privacy remains perfectly protected!** 📱🛡️✨

---

*Designed specifically for the GrapheneOS privacy and security community*
