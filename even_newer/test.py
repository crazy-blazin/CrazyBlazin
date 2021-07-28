# OS modules
import os
import shutil

# Image modules
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# create/delete our temp files folder
if os.path.exists('frames'):
    shutil.rmtree('frames')
os.mkdir('frames')

# load in the background image
img_background = Image.open('background.png')
img = Image.new("RGBA", img_background.size, (0, 0, 0, 255))

# set up colours and vars
x = 10
y = 10
silver = (100, 100, 100, 255)
purple = (100, 0, 200, 255)
white = (255, 255, 255, 255)
black = (0, 0, 0, 0)

name = 'Boomerman'
price = 5000

text_name = f"{name}"
text_price = f"Looted {price} CBS!!!!"

# load the font
font = ImageFont.truetype("ShortBaby-Mg2w.ttf", 60)
draw = ImageDraw.Draw(img)

# add text to each frame
for N in range(0, 50):
    img.paste(img_background, (0, 0))
    draw.text((x+110, y), text_name, black, font=font)
    draw.text((x, y+350), text_price, black, font=font)
    # draw.text((x, y), text_name, silver, font=font)
    # draw.text((x, y), text_name, white, font=font)

    if N%7 == 0:
        draw.text((x+110, y), text_name, white, font=font)
        draw.text((x, y+350), text_price, white, font=font)
    # draw.text((x+10, y+10), text_price, silver, font=font)
    # draw.text((x+10, y+10), text_price, white, font=font)
    img.save("./frames/{}.png".format(str(N).zfill(3)))

# output the result
os.system('ffmpeg -framerate 24 -i frames/%03d.png -c:v ffv1 -r 24 -y out.avi')
os.system('ffmpeg -y -i out.avi out.gif')

# clean up
shutil.rmtree('frames')