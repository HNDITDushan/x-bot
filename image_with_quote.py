from PIL import Image, ImageDraw, ImageFont
import textwrap
import random

def generate_image_with_quote(quote, author):
    # -----------------------------
    # SETTINGS
    # -----------------------------
    WIDTH, HEIGHT = 1024, 1024

    # Use your own fonts (recommended)
    FONT_BOLD = "arialbd.ttf"   # Bold font
    FONT_REG = "arial.ttf"      # Regular font

    # -----------------------------
    # CREATE GRADIENT BACKGROUND
    # -----------------------------
    def create_gradient():
        base = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
        top_color = random.choice([
            (52, 152, 219),
            (155, 89, 182),
            (231, 76, 60),
            (46, 204, 113),
            (241, 196, 15)
        ])
        bottom_color = (20, 20, 20)

        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)

            for x in range(WIDTH):
                base.putpixel((x, y), (r, g, b))

        return base

    img = create_gradient()
    draw = ImageDraw.Draw(img)

    # -----------------------------
    # LOAD FONTS
    # -----------------------------
    quote_font = ImageFont.truetype(FONT_BOLD, 48)
    author_font = ImageFont.truetype(FONT_REG, 32)

    # -----------------------------
    # FORMAT TEXT
    # -----------------------------
    wrapped_quote = textwrap.fill(quote, width=30)

    # Calculate quote size
    bbox = draw.textbbox((0, 0), wrapped_quote, font=quote_font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Center position
    x = (WIDTH - text_w) // 2
    y = (HEIGHT - text_h) // 2 - 40

    # -----------------------------
    # DRAW QUOTE
    # -----------------------------
    draw.text((x, y), wrapped_quote, font=quote_font, fill=(255, 255, 255))

    # -----------------------------
    # DRAW AUTHOR
    # -----------------------------
    author_text = f"— {author}"
    bbox_author = draw.textbbox((0, 0), author_text, font=author_font)
    author_w = bbox_author[2] - bbox_author[0]

    author_x = (WIDTH - author_w) // 2
    author_y = y + text_h + 30

    draw.text((author_x, author_y), author_text, font=author_font, fill=(200, 200, 200))

    watermark_text = "@619Sniper619"

    watermark_font = ImageFont.truetype("arial.ttf", 28)

    bbox = draw.textbbox((0, 0), watermark_text, font=watermark_font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = WIDTH - w - 30
    y = HEIGHT - h - 30

    draw.text((x, y), watermark_text, font=watermark_font, fill=(255, 255, 255, 120))

    # -----------------------------
    # SAVE IMAGE
    # -----------------------------
    img.save("img/quote_pro.png")

    print("✅ Professional quote image created!")