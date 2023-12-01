import re
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# create card
"""
'name'
'profession'
'hobby'
'situation'
'difficulties'
'communication'
'additional'

Example use: 
create_card(name="Jack", profession="driver", hobby="go for walks",  difficulties="hear")

"""


def create_card(**kwargs):
    if not kwargs:
        return "Please provide more information about yourself to create a card."
    name = f'My name is {kwargs["name"]}.' if "name" in kwargs else ""
    profession = f"I am/was a {kwargs['profession']}." if "profession" in kwargs else ""
    hobby = f'In my free time I like to {kwargs["hobby"]}.' if "hobby" in kwargs else ""
    situation = ""
    difficulties = ""
    if "situation" in kwargs and "difficulties" in kwargs:
        situation = f'I {kwargs["situation"]} and it\'s now hard for me to '
        difficulties = f'{kwargs["difficulties"]}.'
    elif "situation" in kwargs:
        situation = f'I {kwargs["situation"]}.'
    elif "difficulties" in kwargs:
        difficulties = f'It\'s now hard for me to {kwargs["difficulties"]}.'

    communication = (
        f'Please help me by {kwargs["communication"]}.'
        if "communication" in kwargs
        else ""
    )
    additional = f'\n {kwargs["additional"]}' if "additional" in kwargs else ""
    s = f"""Hi!
{name}{profession}{hobby} 
{situation}{difficulties}
{communication}
Thank you! {additional}"""

    background_styles = {
        "style1": "style1",
        "style2": "style2",
        "style3": "style3",
        # Add more styles if needed
    }

    # Select the background image based on the 'background-style' argument
    background_style = kwargs["background_style"]
    print(background_style)
    background_image_path = background_styles.get(background_style) + ".png"

    # Load the selected background image
    background = Image.open(background_image_path)
    if background.mode != "RGBA":
        background = background.convert("RGBA")
        white_bg = Image.new("RGBA", background.size, (255, 255, 255, 255))
        white_bg.paste(background, (0, 0), background)
        background = white_bg
    card_width, card_height = background.size
    draw = ImageDraw.Draw(background)

    # Choose a font

    font_size = int(card_height * 0.03)
    font = ImageFont.load_default(font_size)

    # Dynamic starting position based on card size
    x_start = card_width * 0.15  # Example: Start 5% from the left
    y_start = card_height * 0.15  # Example: Start 5% from the top
    if background_style == "style2":
        x_start = card_width * 0.15  # Example: Start 5% from the left
        y_start = card_height * 0.3

    # Current y position, starting from y_start
    current_x, current_y = x_start, y_start

    # Splitting the text into lines
    lines = s.split("\n")
    for line in lines:
        words = line.split()
        current_line = ""
        for word in words:
            # Check the width of the line with the new word
            test_line = f"{current_line} {word}".strip()
            width = draw.textlength(test_line, font=font)
            if width > card_width - 2 * x_start:
                # If line is too long, draw the current line and start a new one
                draw.text((current_x, current_y), current_line, font=font, fill="black")
                current_y += font_size * 1.5  # Adjust line spacing based on font size
                current_line = word
            else:
                current_line = test_line

        # Draw the last line
        draw.text((current_x, current_y), current_line, font=font, fill="black")
        current_y += font_size * 1.5  # Adjust line spacing based on font size

    # Create an in-memory bytes buffer
    img_io = BytesIO()
    background.save(img_io, "PNG")
    img_io.seek(0)  # Go to the beginning of the IO stream

    return img_io


def extract_info_from_card(card_info: str):
    base = set(card_info.split("."))
    info = {}
    for s in base:
        if "My name" in s:
            info["name"] = s.split("name is")[1].strip()
            continue
        if "I am/was" in s:
            info["profession"] = s.split("am/was a")[1].strip()
            continue
        if "free time" in s:
            info["hobby"] = s.split("I like to")[1].strip()
            continue
        if "now hard" in s:
            info["difficulties"] = s.split("now hard for me to")[1].strip()
            if "it's" in s:
                info["situation"] = s.split("and it's now")[0][3:].strip()
            continue
        if "Please" in s:
            info["communication"] = s.split("help me by")[1].strip()
            continue
        if "Thank you" in s:
            l = s.split("!")[1:]
            if " ".join(l).strip():
                info["additional"] = " ".join(l).strip().strip()

    return info
