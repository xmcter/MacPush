#!/usr/bin/env python3
"""Create .DS_Store for DMG using the CORRECT alias extracted from mounted DMG."""

import os
import plistlib

import ds_store
from ds_store import DSStore


def create_ds_store(output_path, staging_dir):
    """Create .DS_Store with correct background alias."""

    # Load the correct alias that was extracted from a real mounted DMG
    alias_file = os.path.join(os.path.dirname(staging_dir), ".correct_alias.bin")
    with open(alias_file, "rb") as f:
        alias_bytes = f.read()

    print(f"Using correct alias: {len(alias_bytes)} bytes")

    with DSStore.open(output_path, "w+") as d:
        bwsp = {
            "WindowBounds": {"TopWindow_1": {"top": 100, "left": 100, "bottom": 500, "right": 760}},
            "ShowPathbar": False,
            "ShowSidebar": False,
            "ShowToolbar": False,
            "SidebarWidth": 0,
            "ContainerShowSidebar": False,
            "ContainerShowToolbar": False,
            "ContainerShowPathbar": False,
            "MainColumnWidth": 660,
        }

        icvp = {
            "viewOptionsVersion": 1,
            "backgroundType": 2,
            "backgroundImageAlias": alias_bytes,
            "iconSize": 80.0,
            "arrangeBy": "none",
            "gridSpacing": 100.0,
            "gridOffsetX": 0.0,
            "gridOffsetY": 0.0,
            "labelOnBottom": True,
            "showIconPreview": True,
            "textSize": 13.0,
            "iconLabelLocation": "bottom",
            "showItemInfo": False,
        }

        d["."]["bwsp"] = ("bplist", plistlib.dumps(bwsp, fmt=plistlib.FMT_BINARY))
        d["."]["icvp"] = ("bplist", plistlib.dumps(icvp, fmt=plistlib.FMT_BINARY))
        d["MacPush.app"]["Iloc"] = (150, 170)
        d["Applications"]["Iloc"] = (510, 170)

    print(f"Created {output_path}")


if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    staging_dir = os.path.join(project_dir, "dmg_staging")
    output_path = os.path.join(staging_dir, ".DS_Store")
    create_ds_store(output_path, staging_dir)
