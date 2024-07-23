from os import path
import os
from PIL import Image, ImageDraw,ImageFont


def current_folder(file_name):
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    return path.join(d, file_name)

img=Image.open(current_folder(r"style\Fin.jpg")).convert("L")
w,h=img.size
pixel_flag=[[True for x in range(w)] for y in range(h)]
threshold=20
canvas_img=Image.new(mode="RGB",size=(w,h),color=(255,0,0))
canvas=ImageDraw.Draw(canvas_img)

print(h,w)
step=10
factor=0.1
for y in range(h):
    print("row",y)
    for x in range(w):
        # tmp=canvas_img.getpixel((x,y))
        # if(pixel_flag[y][x]==False): print(x,y)
        if( pixel_flag[y][x]!=False):
            mean=img.getpixel((x,y))
            pc=step# pixel count
            deviant=0
            # prevh,prevw,prevd=mean,mean,mean
            while(y+pc<h and x+pc<w):
                    pixh=img.getpixel((x+pc,y))
                    # print(x,y+pc,h,w)
                    pixw=img.getpixel((x,y+pc))
                    pixd=img.getpixel((x+pc,y+pc))
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
                font = ImageFont.truetype(current_folder(r"txt\Pistilli-Roman.otf"), pc)
                # canvas.rectangle((x,y,x+pc,y+pc),fill=(mean,mean,mean))
                canvas.text((x+pc//10,y+pc//10), "C", fill=0,font=font)

canvas_img.show()

