import os
import sys 
import time
import logging
import spidev as SPI
import flask
from flask import Flask, request

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
   
################# Definitions for screens ########################        
def create_startup_animation(disp):
    animation_frames = []
    font = ImageFont.truetype("Font/Font02.ttf", 35)
    for i in range(0, 360, 5):
        frame = Image.new("RGB", (disp.width, disp.height), "BLACK")
        draw = ImageDraw.Draw(frame)
        draw.arc((25, 25, 215, 215), 0, 360, fill=(255, 255, 255), width=5)
        draw.arc((25, 25, 215, 215), 0, i, fill=(0, 255, 0), width=5)
        draw.text((disp.width // 2 - 75, disp.height // 2 - 20), "Loading...", fill=(255, 255, 255), font=font)
        animation_frames.append(frame)
    return animation_frames
def create_dndimage(text3, text4, color = (255,255,255)):
    dndimage = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(dndimage)
    draw.arc((1,1,239,239),0, 360, fill = (188,47,73),width = 20)
    draw.arc((2,2,238,238),0, 360, fill = (188,47,73),width = 20)
    draw.arc((3,3,237,237),0, 360, fill = (188,47,73),width = 20)
    draw.line([(40,120),(200,120)],fill = (188,47,73),width = 20)
    Font1 = ImageFont.truetype("Font/Font01.ttf",25)
    Font2 = ImageFont.truetype("Font/Font01.ttf",35)
    Font3 = ImageFont.truetype("Font/Font02.ttf",32)
    draw.text((81, 70), text3, fill = color,font = Font3)
    draw.text((80, 130), text4, fill = color,font = Font3)
    return dndimage.rotate(0)
    
def create_busyimage(text1, color = (255,255,255)):
    busyimage = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(busyimage)
    draw.ellipse((10, 10, disp.width-10, disp.height-10), fill=(188,47,73))
    Font3 = ImageFont.truetype("Font/Font02.ttf",32)
    text_width, text_height = draw.textsize(text1, font=Font3)
    draw.text(((disp.width-text_width)/2, (disp.height-text_height)/2), text1, fill = color,font = Font3)
    return busyimage.rotate(0)
    
def create_availableimage(text1, color = (0,0,0)):
    availableimage = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(availableimage)
    draw.ellipse((10, 10, disp.width-10, disp.height-10), fill=(118, 165, 38))
    Font3 = ImageFont.truetype("Font/Font02.ttf",32)
    text_width, text_height = draw.textsize(text1, font=Font3)
    draw.text(((disp.width-text_width)/2, (disp.height-text_height)/2), text1, fill = color,font = Font3)
    return availableimage.rotate(0)    
    
def create_awayimage(text1, color = (0,0,0)):
    awayimage = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(awayimage)
    draw.ellipse((10, 10, disp.width-10, disp.height-10), fill=(252, 209, 22))
    Font3 = ImageFont.truetype("Font/Font02.ttf",32)
    text_width, text_height = draw.textsize(text1, font=Font3)
    draw.text(((disp.width-text_width)/2, (disp.height-text_height)/2), text1, fill = color,font = Font3)
    return awayimage.rotate(0)      
    
def create_offline(text1, color = (68,71,145)):
    offline = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(offline)
    draw.arc((1,1,239,239),0, 360, fill = (68,71,145),width = 20)
    draw.arc((2,2,238,238),0, 360, fill = (68,71,145),width = 20)
    draw.arc((3,3,237,237),0, 360, fill = (68,71,145),width = 20)
    Font3 = ImageFont.truetype("Font/Font02.ttf",32)
    text_width, text_height = draw.textsize(text1, font=Font3)
    draw.text(((disp.width-text_width)/2, (disp.height-text_height)/2), text1, fill = color,font = Font3)
    return offline.rotate(0)     
    
    
def waitingimage(text1, color = (68,71,145)):
    waiting = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(waiting)
    draw.arc((1,1,239,239),0, 360, fill = (68,71,145),width = 20)
    draw.arc((2,2,238,238),0, 360, fill = (68,71,145),width = 20)
    draw.arc((3,3,237,237),0, 360, fill = (68,71,145),width = 20)
    Font3 = ImageFont.truetype("Font/Font02.ttf",32)
    text_width, text_height = draw.textsize(text1, font=Font3)
    draw.text(((disp.width-text_width)/2, (disp.height-text_height)/2), text1, fill = color,font = Font3)
    return waiting.rotate(0)     

def create_onthephone_image(text1, color=(255, 255, 255)):
    onthephone = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(onthephone)
    draw.ellipse((10, 10, disp.width-10, disp.height-10), fill=(188,47,73))
    Font3 = ImageFont.truetype("Font/Font02.ttf", 32)
    draw.text((30, 100), "On             the", fill=color, font=Font3)
    draw.text((90, 145), "Phone", fill=color, font=Font3)
    phone_image = Image.open("phone.png").resize((80, 80), Image.ANTIALIAS).rotate(90)
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
    disp.ShowImage(image)    
    return 'Showing image: {}'.format(image_type)
    time.sleep(1.5)
############ main ################
if __name__ == '__main__':
    show_startup_animation(disp)
    
    text1 = ('Waiting...')
    image = waitingimage(text1) 
    disp.ShowImage(image)   
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
