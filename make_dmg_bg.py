#!/usr/bin/env python3
"""Generate DMG background image with bilingual (CN/EN) drag instructions."""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 660, 400

# Colors
BG_TOP = (245, 247, 250)
BG_BOTTOM = (225, 230, 238)
TEXT_COLOR = (60, 60, 67)
ARROW_COLOR = (120, 130, 145)
HINT_COLOR = (140, 145, 155)

# Fonts
try:
    font_cn = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 22)
    font_cn_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 13)
except Exception:
    font_cn = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 22)
    font_cn_small = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 13)

try:
    font_en = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    font_en_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 13)
except Exception:
    font_en = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 22)
    font_en_small = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 13)


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def draw_gradient(draw, width, height, top, bottom):
    for y in range(height):
        color = lerp_color(top, bottom, y / max(height - 1, 1))
        draw.line([(0, y), (width, y)], fill=color)


def draw_arrow(draw, x1, y1, x2, y2, color, width=3):
    """Draw a simple right-pointing arrow from (x1,y1) to (x2,y2)."""
    # Shaft
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    # Arrowhead
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 14
    spread = 0.5
    left_x = x2 - arrow_len * math.cos(angle - spread)
    left_y = y2 - arrow_len * math.sin(angle - spread)
    right_x = x2 - arrow_len * math.cos(angle + spread)
    right_y = y2 - arrow_len * math.sin(angle + spread)
    draw.polygon([(x2, y2), (int(left_x), int(left_y)), (int(right_x), int(right_y))], fill=color)


def draw_app_icon_placeholder(draw, cx, cy, size=80):
    """Draw a simple rounded-rect app icon placeholder."""
    x0, y0 = cx - size // 2, cy - size // 2
    x1, y1 = cx + size // 2, cy + size // 2
    radius = 18
    # Shadow
    draw.rounded_rectangle([x0 + 3, y0 + 6, x1 + 3, y1 + 6], radius=radius, fill=(0, 0, 0, 30))
    # Icon body - dark gradient bell color
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=(50, 55, 65))
    # Bell shape (simplified)
    bell_w = size * 0.5
    bell_h = size * 0.45
    bx0 = cx - bell_w / 2
    by0 = cy - bell_h / 2 + 2
    bx1 = cx + bell_w / 2
    by1 = cy + bell_h / 2
    # Bell body
    draw.ellipse([bx0, by0, bx1, by1], fill=(255, 255, 255))
    # Bell top
    draw.ellipse([cx - 4, by0 - 8, cx + 4, by0], fill=(255, 255, 255))
    # Bell bottom strip
    draw.rounded_rectangle([bx0 - 2, by1 - 4, bx1 + 2, by1 + 2], radius=2, fill=(255, 255, 255))
    # Clapper
    draw.ellipse([cx - 5, by1 + 2, cx + 5, by1 + 12], fill=(255, 255, 255))


def draw_folder_icon_placeholder(draw, cx, cy, size=80):
    """Draw a simple Applications folder placeholder."""
    x0, y0 = cx - size // 2, cy - size // 2
    x1, y1 = cx + size // 2, cy + size // 2
    radius = 10
    # Shadow
    draw.rounded_rectangle([x0 + 3, y0 + 6, x1 + 3, y1 + 6], radius=radius, fill=(0, 0, 0, 30))
    # Folder back
    draw.rounded_rectangle([x0, y0, x1, y0 + 22], radius=radius, fill=(120, 170, 230))
    draw.rectangle([x0, y0 + 10, x1, y0 + 22], fill=(120, 170, 230))
    # Folder front
    draw.rounded_rectangle([x0, y0 + 18, x1, y1], radius=radius, fill=(150, 200, 255))
    draw.rectangle([x0, y0 + 18, x1, y0 + 28], fill=(150, 200, 255))


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # Gradient background
    draw_gradient(draw, W, H, BG_TOP, BG_BOTTOM)

    # Title
    title_cn = "拖拽 MacPush.app 到 Applications 文件夹"
    title_en = "Drag MacPush.app to the Applications folder"

    # Measure text
    bbox_cn = draw.textbbox((0, 0), title_cn, font=font_cn)
    bbox_en = draw.textbbox((0, 0), title_en, font=font_en)
    w_cn = bbox_cn[2] - bbox_cn[0]
    w_en = bbox_en[2] - bbox_en[0]

    # Draw centered text (Chinese on top, English below)
    y_text = 40
    draw.text(((W - w_cn) / 2, y_text), title_cn, fill=TEXT_COLOR, font=font_cn)
    y_text += 32
    draw.text(((W - w_en) / 2, y_text), title_en, fill=TEXT_COLOR, font=font_en)

    # Icons positions
    icon_y = 220
    app_x = 150
    folder_x = W - 150

    # Draw placeholders
    draw_app_icon_placeholder(draw, app_x, icon_y, size=90)
    draw_folder_icon_placeholder(draw, folder_x, icon_y, size=90)

    # Labels under icons
    app_label = "MacPush.app"
    folder_label = "Applications"
    bbox_app = draw.textbbox((0, 0), app_label, font=font_en_small)
    bbox_folder = draw.textbbox((0, 0), folder_label, font=font_en_small)
    w_app = bbox_app[2] - bbox_app[0]
    w_folder = bbox_folder[2] - bbox_folder[0]
    draw.text((app_x - w_app / 2, icon_y + 55), app_label, fill=HINT_COLOR, font=font_en_small)
    draw.text((folder_x - w_folder / 2, icon_y + 55), folder_label, fill=HINT_COLOR, font=font_en_small)

    # Arrow between icons
    arrow_y = icon_y
    draw_arrow(draw, app_x + 60, arrow_y, folder_x - 60, arrow_y, ARROW_COLOR, width=3)

    # Bottom hint
    hint_cn = "安装完成后，在「应用程序」文件夹中启动 MacPush"
    hint_en = "After installation, launch MacPush from the Applications folder"
    bbox_hcn = draw.textbbox((0, 0), hint_cn, font=font_cn_small)
    bbox_hen = draw.textbbox((0, 0), hint_en, font=font_en_small)
    w_hcn = bbox_hcn[2] - bbox_hcn[0]
    w_hen = bbox_hen[2] - bbox_hen[0]
    y_hint = H - 50
    draw.text(((W - w_hcn) / 2, y_hint), hint_cn, fill=HINT_COLOR, font=font_cn_small)
    draw.text(((W - w_hen) / 2, y_hint + 20), hint_en, fill=HINT_COLOR, font=font_en_small)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dmg_background.png")
    img.save(output_path, "PNG")
    print(f"Saved {output_path} (660x400, bilingual)")


if __name__ == "__main__":
    main()
