import os
import sys 
import time
import logging
import spidev as SPI
import flask
from flask import Flask, request
sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont

app = Flask(__name__)


# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level = logging.DEBUG)

# display with hardware SPI:
disp = LCD_1inch28.LCD_1inch28()
# Initialize library.
disp.Init()
# Clear display.
disp.clear()
   
        
def create_dndimage(text3, text4, color = (255,255,255)):
    dndimage = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(dndimage)
    draw.arc((1,1,239,239),0, 360, fill = (255,0,0),width = 20)
    draw.arc((2,2,238,238),0, 360, fill = (255,0,0),width = 20)
    draw.arc((3,3,237,237),0, 360, fill = (255,0,0),width = 20)
    draw.line([(40,120),(200,120)],fill = (255,0,0),width = 20)
    Font1 = ImageFont.truetype("../Font/Font01.ttf",25)
    Font2 = ImageFont.truetype("../Font/Font01.ttf",35)
    Font3 = ImageFont.truetype("../Font/Font02.ttf",32)
    draw.text((81, 70), text3, fill = color,font = Font3)
    draw.text((80, 130), text4, fill = color,font = Font3)
    return dndimage.rotate(0)
    
def create_busyimage(text1, color = (255,255,255)):
    busyimage = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(busyimage)
    draw.ellipse((10, 10, disp.width-10, disp.height-10), fill=(255, 0, 0))
    Font3 = ImageFont.truetype("../Font/Font02.ttf",32)
    text_width, text_height = draw.textsize(text1, font=Font3)
    draw.text(((disp.width-text_width)/2, (disp.height-text_height)/2), text1, fill = color,font = Font3)
    return busyimage.rotate(0)
    
def create_availableimage(text1, color = (0,0,0)):
    availableimage = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(availableimage)
    draw.ellipse((10, 10, disp.width-10, disp.height-10), fill=(0, 235, 0))
    Font3 = ImageFont.truetype("../Font/Font02.ttf",32)
    text_width, text_height = draw.textsize(text1, font=Font3)
    draw.text(((disp.width-text_width)/2, (disp.height-text_height)/2), text1, fill = color,font = Font3)
    return availableimage.rotate(0)    



@app.route('/')
def index():
    return 'Hello World'

@app.route('/showimage', methods=['POST'])
def showimage():
    global stop_animation
    stop_animation = True
    image_type = request.form.get('image_type')
    if image_type == 'dnd':
        text3 = request.form.get('text1')
        text4 = request.form.get('text2')
        image = create_dndimage(text3, text4)
    elif image_type == 'busy':
        text1 = request.form.get('text1')
        image = create_busyimage(text1)
    elif image_type == 'available':
        text1 = request.form.get('text1')
        image = create_availableimage(text1)
    disp.ShowImage(image)    
    return 'Showing image: {}'.format(image_type)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)