#!/bin/bash
set -e

PROJECT_DIR="/Users/a123/WorkBuddy/2026-06-18-22-17-26/MacPush"
STAGE="${PROJECT_DIR}/dmg_staging"
FINAL_DMG="${PROJECT_DIR}/MacPush.dmg"

echo "=== Building MacPush.dmg (with background) ==="

# Clean up old files
rm -f "${FINAL_DMG}"
rm -rf "${STAGE}"

# Create staging directory
mkdir -p "${STAGE}/.background"

# Copy app and resources
cp -R "${PROJECT_DIR}/MacPush.app" "${STAGE}/"
ln -s /Applications "${STAGE}/Applications"
cp "${PROJECT_DIR}/dmg_background.png" "${STAGE}/.background/dmg_background.png"

# Generate .DS_Store with CORRECT alias (previously extracted from mounted DMG)
echo "Generating .DS_Store..."
/Users/a123/.workbuddy/binaries/python/versions/3.13.12/bin/python3 "${PROJECT_DIR}/create_ds_store.py"

echo "Staging contents:"
ls -la "${STAGE}"

# Create compressed DMG directly from staging directory
echo ""
echo "Creating compressed DMG..."
hdiutil create -ov -volname "MacPush" -fs HFS+ -srcfolder "${STAGE}" \
    -format UDZO -imagekey zlib-level=9 -o "${FINAL_DMG}"

# Clean up staging
rm -rf "${STAGE}"

echo ""
echo "=== Done! ==="
ls -lh "${FINAL_DMG}"
