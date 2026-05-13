"""生成 JSON Tool 应用图标"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 圆角矩形背景 - 深蓝渐变色
    r = 48  # 圆角半径
    bg_color = (15, 23, 42)  # #0f172a
    draw.rounded_rectangle([(0, 0), (size - 1, size - 1)], radius=r, fill=bg_color)

    # 内部装饰圆角矩形 (略小，形成边框感)
    inner_margin = 12
    inner_r = 38
    inner_color = (30, 41, 59)  # #1e293b
    draw.rounded_rectangle(
        [(inner_margin, inner_margin), (size - inner_margin - 1, size - inner_margin - 1)],
        radius=inner_r, fill=inner_color
    )

    # 绘制 { } 花括号 - 使用蓝色高亮
    brace_color = (59, 130, 246)  # #3b82f6 (accent blue)

    # 左花括号 {
    lx = 62
    # 左花括号的三段：上横线、中竖线、下横线
    draw.line([(lx + 28, 72), (lx + 12, 72)], fill=brace_color, width=10)
    draw.line([(lx + 12, 72), (lx + 12, 118)], fill=brace_color, width=10)
    draw.line([(lx + 12, 118), (lx, 128)], fill=brace_color, width=10)
    draw.line([(lx, 128), (lx + 12, 138)], fill=brace_color, width=10)
    draw.line([(lx + 12, 138), (lx + 12, 184)], fill=brace_color, width=10)
    draw.line([(lx + 12, 184), (lx + 28, 184)], fill=brace_color, width=10)

    # 右花括号 }
    rx = 194
    draw.line([(rx - 28, 72), (rx - 12, 72)], fill=brace_color, width=10)
    draw.line([(rx - 12, 72), (rx - 12, 118)], fill=brace_color, width=10)
    draw.line([(rx - 12, 118), (rx, 128)], fill=brace_color, width=10)
    draw.line([(rx, 128), (rx - 12, 138)], fill=brace_color, width=10)
    draw.line([(rx - 12, 138), (rx - 12, 184)], fill=brace_color, width=10)
    draw.line([(rx - 12, 184), (rx - 28, 184)], fill=brace_color, width=10)

    # 中间的 JSON 文字
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 32)
    except OSError:
        font = ImageFont.load_default()

    text = "JSON"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (size - tw) // 2
    ty = (size - th) // 2 - 8
    draw.text((tx, ty), text, fill=(248, 250, 252), font=font)  # #f8fafc

    # 底部小字 "TOOL"
    try:
        font_small = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20)
    except OSError:
        font_small = ImageFont.load_default()

    text2 = "TOOL"
    bbox2 = draw.textbbox((0, 0), text2, font=font_small)
    tw2 = bbox2[2] - bbox2[0]
    tx2 = (size - tw2) // 2
    ty2 = ty + th + 4
    draw.text((tx2, ty2), text2, fill=(148, 163, 184), font=font_small)  # #94a3b8

    # 生成多尺寸 .ico
    sizes = [16, 32, 48, 64, 128, 256]
    icons = [img.resize((s, s), Image.LANCZOS) for s in sizes]

    ico_path = os.path.join(os.path.dirname(__file__), "icon.ico")
    icons[0].save(ico_path, format="ICO", sizes=[(s, s) for s in sizes], append_images=icons[1:])
    print(f"图标已生成: {ico_path}")

    # 同时保存一份 PNG 预览
    png_path = os.path.join(os.path.dirname(__file__), "icon.png")
    img.save(png_path)
    print(f"PNG 预览: {png_path}")

if __name__ == "__main__":
    create_icon()
