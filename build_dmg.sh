#!/bin/bash
set -e

PROJECT_DIR="/Users/a123/WorkBuddy/2026-06-18-22-17-26/MacPush"
STAGE="${PROJECT_DIR}/dmg_staging"
FINAL_DMG="${PROJECT_DIR}/MacPush.dmg"
TEST_DMG="${PROJECT_DIR}/MacPush_test.dmg"

# Clean up old DMGs
rm -f "${FINAL_DMG}" "${TEST_DMG}"

# Ensure staging directory is clean and set up
rm -rf "${STAGE}"
mkdir -p "${STAGE}/.background"

# Copy app
cp -R "${PROJECT_DIR}/MacPush.app" "${STAGE}/"

# Create Applications symlink
ln -s /Applications "${STAGE}/Applications"

# Copy background image
cp "${PROJECT_DIR}/dmg_background.png" "${STAGE}/.background/dmg_background.png"

# Create .DS_Store with background and icon positions
/Users/a123/.workbuddy/binaries/python/versions/3.13.12/bin/python3 "${PROJECT_DIR}/create_ds_store.py"

echo "Staging directory contents:"
ls -la "${STAGE}"
echo ""
echo "Symlink check:"
ls -la "${STAGE}/Applications"
echo ""
echo ".DS_Store check:"
ls -la "${STAGE}/.DS_Store"

# Create compressed DMG directly from staging directory
echo ""
echo "Creating compressed DMG..."
hdiutil create -ov -volname "MacPush" -fs HFS+ -srcfolder "${STAGE}" -format UDZO -imagekey zlib-level=9 -o "${FINAL_DMG}"

# Clean up staging
rm -rf "${STAGE}"

echo ""
echo "=== Done! ==="
ls -lh "${FINAL_DMG}"
