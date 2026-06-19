#!/bin/bash
set -e

echo "=== Starting MacPush App Build ==="

# Clean old builds
rm -rf MacPush.app
rm -f MenuBarApp

# Compile the native Objective-C app with WebKit linked
echo "Compiling Objective-C wrapper..."
clang -framework Cocoa -framework Foundation -framework WebKit -o MenuBarApp MenuBarApp.m -fobjc-arc

# Create the standard App bundle directory structure
echo "Creating app directory structure..."
mkdir -p MacPush.app/Contents/MacOS
mkdir -p MacPush.app/Contents/Resources/web

# Move the executable
mv MenuBarApp MacPush.app/Contents/MacOS/MacPush

# Copy Python scripts to the bundle Resources directory
echo "Packing python helper daemons..."
cp forwarder.py MacPush.app/Contents/Resources/
cp config_helper.py MacPush.app/Contents/Resources/
cp web_config.py MacPush.app/Contents/Resources/

# Copy the web assets to the bundle Resources web directory
echo "Packing Web UI assets..."
cp web/index.html MacPush.app/Contents/Resources/web/
cp web/style.css MacPush.app/Contents/Resources/web/
cp web/app.js MacPush.app/Contents/Resources/web/

# Copy the app icon to the bundle Resources directory
if [ -f "app_icon.icns" ]; then
    echo "Packing App Icon..."
    cp app_icon.icns MacPush.app/Contents/Resources/
fi

# Write the Info.plist
echo "Writing Info.plist..."
cat > MacPush.app/Contents/Info.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>MacPush</string>
    <key>CFBundleIdentifier</key>
    <string>com.a123.macpush</string>
    <key>CFBundleName</key>
    <string>MacPush</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleIconFile</key>
    <string>app_icon.icns</string>
    <key>LSUIElement</key>
    <true/>
</dict>
</plist>
EOF

# Ad-hoc code sign (required for Gatekeeper, no Apple Developer certificate needed)
echo "Code signing (ad-hoc)..."
codesign --force --deep --sign - MacPush.app

echo "=== Build completed successfully! ==="
echo "The application bundle is at: ./MacPush.app"
echo ""
echo "To install to /Applications:"
echo "  cp -R MacPush.app /Applications/"
