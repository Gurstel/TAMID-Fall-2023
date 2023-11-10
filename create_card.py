import re
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
# create card
'''
'name'
'profession'
'hobby'
'situation'
'difficulties'
'communication'
'additional'

Example use: 
create_card(name="Jack", profession="driver", hobby="go for walks",  difficulties="hear")

'''


def create_card(**kwargs):
    if not kwargs:
        return "Please provide more information about yourself to create a card."
    name = f'My name is {kwargs["name"]}.' if 'name' in kwargs else ""
    profession = f"I am/was a {kwargs['profession']}." if 'profession' in kwargs else ""
    hobby = f'In my free time I like to {kwargs["hobby"]}.' if "hobby" in kwargs else ''
    situation = ''
    difficulties = ''
    if 'situation' in kwargs and 'difficulties' in kwargs:
        situation = f'I {kwargs["situation"]} and it\'s now hard for me to '
        difficulties = f'{kwargs["difficulties"]}.'
    elif 'situation' in kwargs:
        situation = f'I {kwargs["situation"]}.'
    elif 'difficulties' in kwargs:
        difficulties = f'It\'s now hard for me to {kwargs["difficulties"]}.'

    communication = f'Please help me by {kwargs["communication"]}.' if "communication" in kwargs else ''
    additional = f'\n {kwargs["additional"]}' if 'additional' in kwargs else ''
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
    background_style = kwargs['background_style']
    print(background_style)
    background_image_path = background_styles.get(background_style) + ".png"

    # Load the selected background image
    background = Image.open(background_image_path)
    if background.mode != 'RGBA':
        background = background.convert('RGBA')
        white_bg = Image.new('RGBA', background.size, (255, 255, 255, 255))
        white_bg.paste(background, (0, 0), background)
        background = white_bg
    draw = ImageDraw.Draw(background)

    # Choose a font
    font = ImageFont.load_default()

    # The position where the text drawing will start
    x, y = 10, 10

    # Splitting the text into lines
    lines = s.split('\n')
    for line in lines:
        # Draw the text onto the image
        draw.text((x, y), line, font=font, fill="black")
        y += 30  # Adjust line spacing as necessary

    # Create an in-memory bytes buffer
    img_io = BytesIO()
    background.save(img_io, 'PNG')
    img_io.seek(0)  # Go to the beginning of the IO stream

    return img_io
