import os
import sys 
import time
import logging
import spidev as SPI
import flask
from flask import Flask, request
import threading
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont

# Define a lock object
display_lock = threading.Lock()

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
# Constants

FONT_02 = ImageFont.truetype("Font/Font01.ttf", 32)
FONT_03 = ImageFont.truetype("Font/Font02.ttf", 35)
COLOR_RED = (188, 47, 73)
COLOR_GREEN = (118, 165, 38)
COLOR_YELLOW = (252, 209, 22)
COLOR_BLUE = (68, 71, 145)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

app = Flask(__name__)
   
################# Definitions for screens ########################        
def create_startup_animation(disp):
    animation_frames = []
    font = FONT_02
    for i in range(0, 360, 5):
        frame = Image.new("RGB", (disp.width, disp.height), COLOR_BLACK)
        draw = ImageDraw.Draw(frame)
        draw.arc((25, 25, 215, 215), 0, 360, fill=COLOR_WHITE, width=5)
        draw.arc((25, 25, 215, 215), 0, i, fill=COLOR_GREEN, width=5)
        draw.text(
            (disp.width // 2 - 75, disp.height // 2 - 20),
            "Loading...",
            fill=COLOR_WHITE,
            font=FONT_03,
        )
        animation_frames.append(frame)
    return animation_frames
def create_dndimage(text3, text4, color=COLOR_WHITE):
    dndimage = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(dndimage)
    draw.arc((1, 1, 239, 239), 0, 360, fill=COLOR_RED, width=20)
    draw.arc((2, 2, 238, 238), 0, 360, fill=COLOR_RED, width=20)
    draw.arc((3, 3, 237, 237), 0, 360, fill=COLOR_RED, width=20)
    draw.line([(40, 120), (200, 120)], fill=COLOR_RED, width=20)
    draw.text((81, 70), text3, fill=color, font=FONT_03)
    draw.text((80, 130), text4, fill=color, font=FONT_03)
    return dndimage.rotate(0)
    
def create_busyimage(text1, color=COLOR_WHITE):
    busyimage = Image.new("RGB", (disp.width, disp.height), COLOR_BLACK)
    draw = ImageDraw.Draw(busyimage)
    draw.ellipse((10, 10, disp.width-10, disp.height-10), fill=COLOR_RED)
    text_width, text_height = draw.textsize(text1, font=FONT_03)
    draw.text(
        ((disp.width-text_width)//2, (disp.height-text_height)//2),
        text1,
        fill=color,
        font=FONT_03,
    )
    return busyimage.rotate(0)

def create_availableimage(text1, color=COLOR_BLACK):
    availableimage = Image.new("RGB", (disp.width, disp.height), COLOR_BLACK)
    draw = ImageDraw.Draw(availableimage)
    draw.ellipse((10, 10, disp.width-10, disp.height-10), fill=COLOR_GREEN)
    text_width, text_height = draw.textsize(text1, font=FONT_03)
    draw.text(
        ((disp.width-text_width)//2, (disp.height-text_height)//2),
        text1,
        fill=color,
        font=FONT_03,
    )
    return availableimage.rotate(0)

def create_awayimage(text1, color=COLOR_BLACK):
    awayimage = Image.new("RGB", (disp.width, disp.height), COLOR_BLACK)
    draw = ImageDraw.Draw(awayimage)
    draw.ellipse((10, 10, disp.width-10, disp.height-10), fill=COLOR_YELLOW)
    text_width, text_height = draw.textsize(text1, font=FONT_03)
    draw.text(
        ((disp.width-text_width)//2, (disp.height-text_height)//2),
        text1,
        fill=color,
        font=FONT_03,
    )
    return awayimage.rotate(0)

def create_offline(text1, color=COLOR_BLUE):
    offline = Image.new("RGB", (disp.width, disp.height), COLOR_BLACK)
    draw = ImageDraw.Draw(offline)
    draw.arc((1, 1, 239, 239), 0, 360, fill=COLOR_BLUE, width=20)
    draw.arc((2, 2, 238, 238), 0, 360, fill=COLOR_BLUE, width=20)
    draw.arc((3, 3, 237, 237), 0, 360, fill=COLOR_BLUE, width=20)
    text_width, text_height = draw.textsize(text1, font=FONT_03)
    draw.text(
        ((disp.width-text_width)//2, (disp.height-text_height)//2),
        text1,
        fill=color,
        font=FONT_03,
    )
    return offline.rotate(0)
    
    
def waitingimage(text1, color = (68,71,145)):
    waiting = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(waiting)
    draw.arc((1,1,239,239),0, 360, fill = (68,71,145),width = 20)
    draw.arc((2,2,238,238),0, 360, fill = (68,71,145),width = 20)
    draw.arc((3,3,237,237),0, 360, fill = (68,71,145),width = 20)
    text_width, text_height = draw.textsize(text1, font=FONT_03)
    draw.text(((disp.width-text_width)/2, (disp.height-text_height)/2), text1, fill = color,font = FONT_03)
    return waiting.rotate(0)     

def create_errorimage(text1, text2, color=COLOR_RED):
    errorimage = Image.new("RGB", (disp.width, disp.height), COLOR_BLACK)
    draw = ImageDraw.Draw(errorimage)
    draw.text((20, 50), text1, fill=color, font=FONT_03)
    draw.text((20, 100), text2, fill=color, font=FONT_03)
    return errorimage.rotate(0)
    
def create_onthephone_image(text1, color=(255, 255, 255)):
    onthephone = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(onthephone)
    draw.ellipse((10, 10, disp.width-10, disp.height-10), fill=(188,47,73))
    draw.text((30, 100), "On             the", fill=color, font=FONT_03)
    draw.text((90, 145), "Phone", fill=color, font=FONT_02)
    phone_image = Image.open("phone.png").resize((80, 80), resample=Image.ANTIALIAS).rotate(90)
    onthephone.paste(phone_image, (80, 60), phone_image)
    return onthephone.rotate(0)

        
def show_startup_animation(disp):
    animation_frames = create_startup_animation(disp)
    for frame in animation_frames:
        disp.ShowImage(frame)
        time.sleep(0)
# default route if someone browses, should maybe have some instructions??
@app.route('/')
def index():
    return 'Hello World'

# triggers when posting to /showimage
@app.route('/showimage', methods=['POST'])
def showimage():
    global stop_animation
    stop_animation = True
    if request.method == 'POST':
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
        elif image_type == 'away':
            text1 = request.form.get('text1')
            image = create_awayimage(text1)  
        elif image_type == 'offline':
            text1 = request.form.get('text1')
            image = create_offline(text1)
        elif image_type == 'onthephone':
            text1 = request.form.get('text1')
            image = create_onthephone_image(text1)
        else:
            return 'Invalid image_type'
    else:
        return 'Not a POST request'

    print("Matched image_type:", image_type)       
     # Acquire the lock before drawing to the display
    display_lock.acquire()
    try:
        disp.ShowImage(image)
    finally:
        # Release the lock when done drawing
        display_lock.release()
    
    return 'Showing image: {}'.format(image_type)
############ main ################
if __name__ == '__main__':
    show_startup_animation(disp)
    
    text1 = ('Waiting...')
    image = waitingimage(text1) 
    disp.ShowImage(image)   
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
