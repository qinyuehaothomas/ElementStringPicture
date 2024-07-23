from os import path
import os
from PIL import Image, ImageDraw,ImageFont
from random import randint

def current_folder(file_name):
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    return path.join(d, file_name)

with open(current_folder(r'txt\Element_sorted.txt'),"r") as f:
    Element=f.read().split(',')

def scale(l,v):
    alter=randint(-2,2)
    choice=len(l)-max(0,min(int((v/255)*len(l))+alter,len(l)))-1
    return l[choice]

img=Image.open(current_folder(r"style\Fin.jpg")).convert("L")
w,h=img.size
pixel_flag=[[True for x in range(w)] for y in range(h)]
threshold=20
canvas_img=Image.new(mode="RGB",size=(w,h),color=(255,0,0))
canvas=ImageDraw.Draw(canvas_img)

print(h,w)
step=10
factor=0.2
font_size={1:1,2:1.5}

# need to double the scale of canvas !
for y in range(h):
    print("row",y)
    for x in range(w):
        if( pixel_flag[y][x]):

            # overlap problem
            # The starting block was not flagged, it eats into other boxes
            
            mean=img.getpixel((x,y))
            pc=step# pixel count
            deviant=0
            # prevh,prevw,prevd=mean,mean,mean
            while(y+pc<h and x+pc<w):
                    pixh=img.getpixel((x+pc,y))
                    pixw=img.getpixel((x,y+pc))
                    pixd=img.getpixel((x+pc,y+pc))
                    if(not pixel_flag[y+pc][x+pc]): break
                    if( abs(pixh-mean)+abs(pixw-mean)+abs(pixd-mean)>=threshold+(pc*factor) ):
                        break
                    else:
                        # mean+=pixh+pixw+pixd
                        pc+=step
            if(y+pc>=h or x+pc>=w): pc-=step
            for a in range(pc):
                for b in range(pc):
                    pixel_flag[y+a][x+b]=False
            if(pc!=0):
                res=scale(Element,mean)
                font = ImageFont.truetype(current_folder(r"txt\Pistilli-Roman.otf"), pc/font_size[len(res)])
                bbox= font.getbbox(res)  # Size of text w/font if rendered.
                txt_width ,txt_height = bbox[2]-bbox[0], bbox[3]-bbox[1]
                canvas.rectangle((x,y,x+pc,y+pc),fill=(mean,mean,mean))
                canvas.text(((x+pc//2)-txt_width//2 , (y+pc//2) - txt_height//2), res, fill=0,font=font,align="centre")

# canvas_img.show()
canvas_img.save(current_folder(r"style\_res2.png"))

# should do two rounds with smaller steps!
