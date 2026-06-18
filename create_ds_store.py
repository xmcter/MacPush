#!/usr/bin/env python3
"""Create .DS_Store for DMG with background image and icon positions."""

import os
import plistlib
import datetime

import ds_store
from ds_store import DSStore
from mac_alias import Alias


def create_ds_store(output_path, staging_dir):
    """Create a .DS_Store file that sets background image and icon positions."""

    bg_file = os.path.join(staging_dir, ".background", "dmg_background.png")

    # Create alias from local file, then modify to point to DMG volume
    alias = Alias.for_file(bg_file)

    # Modify volume info to match the DMG volume
    alias.volume.name = b"MacPush"
    alias.volume.posix_path = b"/"
    alias.volume.creation_date = datetime.datetime(2024, 1, 1, tzinfo=alias.volume.creation_date.tzinfo)
    alias.volume.fs_type = b"H+"  # HFS+
    alias.volume.disk_type = 0  # fixed disk
    alias.volume.attribute_flags = 0

    # Modify target info to use path relative to volume root
    alias.target.posix_path = b"/.background/dmg_background.png"
    alias.target.carbon_path = b"MacPush:.background:\x00dmg_background.png"
    alias.target.folder_name = b".background"
    alias.target.filename = b"dmg_background.png"
    # Clear CNID path since it won't match
    alias.target.cnid_path = []
    alias.target.cnid = 0
    alias.target.folder_cnid = 0

    alias_bytes = alias.to_bytes()
    print(f"Alias bytes length: {len(alias_bytes)}")

    # Create the .DS_Store file
    with DSStore.open(output_path, "w+") as d:
        # Window bounds (bwsp)
        bwsp = {
            "WindowBounds": {
                "TopWindow_1": {"top": 100, "left": 100, "bottom": 500, "right": 760}
            },
            "ShowPathbar": False,
            "ShowSidebar": False,
            "ShowToolbar": False,
            "SidebarWidth": 0,
            "ContainerShowSidebar": False,
            "ContainerShowToolbar": False,
            "ContainerShowPathbar": False,
            "MainColumnWidth": 660,
        }

        # Icon view properties (icvp)
        icvp = {
            "viewOptionsVersion": 1,
            "backgroundType": 2,  # 2 = image
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

        # Icon positions
        d["MacPush.app"]["Iloc"] = (150, 170)
        d["Applications"]["Iloc"] = (510, 170)

    print(f"Created {output_path}")


if __name__ == "__main__":
    staging_dir = "/Users/a123/WorkBuddy/2026-06-18-22-17-26/MacPush/dmg_staging"
    output_path = os.path.join(staging_dir, ".DS_Store")
    create_ds_store(output_path, staging_dir)
