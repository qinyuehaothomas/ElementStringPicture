from os import path
import os
from PIL import Image, ImageDraw,ImageFont
from random import randint,choice

# ====================================================================================================================================================
# Define Shits

def current_folder(file_name):
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    return path.join(d, file_name)

with open(current_folder(r'txt\Element_sorted.txt'),"r") as f:
    Element=f.read().split(',')

def scale(l,v):
    alter=choice([-2,-1,0,0,1,2])
    c=len(l)-max(0,min(int((v/255)*len(l))+alter,len(l)))-1
    return l[c]

class txt():
    def __init__(self , word:str  , font_path:str , rect:tuple , fill:tuple) :
        font_size_ref={1:1,2:1.5}
        self.text=word
        self.font_path=font_path
        self.x=None
        self.y=None
        self.rect=rect
        self.font_size=(rect[2]-rect[0])/font_size_ref[len(word)]
        self.fill=fill
    def draw(self,scale:int , canvas:ImageDraw, canvas_img:Image , fill:tuple=(-1,-1,-1) , bg:bool=False,rotate:bool=False):
        #scale
        font = ImageFont.truetype(self.font_path,self.font_size*ENLARGE)
        bbox= font.getbbox(self.text)  # Size of text w/font if rendered.
        txt_width ,txt_height = bbox[2]-bbox[0], bbox[3]-bbox[1]
        txt_l,txt_u=((scale*(self.rect[0]+self.rect[2])//2)-txt_width//2 , (scale*(self.rect[1]+self.rect[3])//2) - txt_height//2)
        if(fill[0]==-1): fill=self.fill
        rect=tuple(map(lambda x:x*scale,self.rect))
        if(bg):canvas.rectangle(rect,fill=self.fill)
        canvas.text((txt_l,txt_u), self.text, fill=self.fill,font=font,align="centre")

        if(rotate):
            rotation=choice([270,0,0,90])
            tmp = canvas_img.crop (rect)
            tmp = tmp.rotate (rotation, expand = 1)
            canvas_img.paste (tmp, (rect[0],rect[1]))


# ====================================================================================================================================================
#Load Shits

img=Image.open(current_folder(r"style\Face.jpg"))
imgl=img.convert("L")
w,h=imgl.size

# ====================================================================================================================================================
# Here onward, First round of Boxxing(big boxes)


pixel_flag=[[True for x in range(w)] for y in range(h)]

ENLARGE=10
TXT=[]

print(h,w)
STEP1=20
LAGRER_FACTOR=0.4
THRESHOLD1=20

# need to double the scale of canvas !
for y in range(h):
    # print("row",y)
    for x in range(w):
        if( pixel_flag[y][x]):
            # overlap problem
            # The starting block was not flagged, it eats into other boxes
            mean=imgl.getpixel((x,y))
            pc=STEP1# pixel count
            # prevh,prevw,prevd=mean,mean,mean
            while(y+pc<h and x+pc<w):
                    pixh=imgl.getpixel((x+pc,y))
                    pixw=imgl.getpixel((x,y+pc))
                    pixd=imgl.getpixel((x+pc,y+pc))
                    if(not pixel_flag[y+pc][x+pc] or not pixel_flag[y][x+pc] or not pixel_flag[y+pc][x]): break
                    if( abs(pixh-mean)+abs(pixw-mean)+abs(pixd-mean)>=THRESHOLD1+(pc*LAGRER_FACTOR) ):
                        break
                    else:
                        # mean+=pixh+pixw+pixd
                        pc+=STEP1
            if(y+pc>=h or x+pc>=w): pc-=STEP1
            RGBmean=[0,0,0]
            for a in range(pc):
                for b in range(pc):
                    pixel_flag[y+a][x+b]=False
                    r,g,b=img.getpixel((x+b,y+a))
                    RGBmean[0]+=r
                    RGBmean[1]+=g
                    RGBmean[2]+=b

            if(pc!=0):
                res=scale(Element,mean)
                TXT.append(txt(
                    res,
                    current_folder(r"txt\Pistilli-Roman.otf"),
                    (x,y,x+pc,y+pc),
                    tuple(map(lambda x: x//(pc*pc),RGBmean))
                ))

canvas_img=Image.new(mode="RGB",size=(w*ENLARGE,h*ENLARGE),color=(255,255,255))
canvas=ImageDraw.Draw(canvas_img)
for todo in TXT:
    todo.draw(ENLARGE,canvas,canvas_img,rotate=True)
    # print(todo.text)

# canvas_img.show()
# canvas_img.save(current_folder(r"style\_res2.png"))
# input("cut")
print("round 1 done")
# ====================================================================================================================================================
# Here onward, Fill empty space

# Second scan based on canvas

pixel_flag=[[True for x in range(w)] for y in range(h)]

TXT2=[]

txt_ref=canvas_img.convert('L').resize((w,h))
# txt_ref.show()
STEP2=1
THRESHOLD1=20

BOX_SIZE_LIM=1 # threshold of box size

def interpolate(x:float):
    return x
    # return min(255,x+10)

print("init done")
# need to double the scale of canvas !
for y in range(h):
    # if(y%10 ==0):print("row",y)
    for x in range(w):
        mean=txt_ref.getpixel((x,y))
        if( mean==255 and  pixel_flag[y][x]):
            mean=imgl.getpixel((x,y))
            # overlap problem
            # The starting block was not flagged, it eats into other boxes
            pc=STEP2# pixel count
            # prevh,prevw,prevd=mean,mean,mean
            while(y+pc<h and x+pc<w):
                    txt_pix_h=txt_ref.getpixel((x+pc,y))
                    txt_pix_w=txt_ref.getpixel((x,y+pc))
                    txt_pix_d=txt_ref.getpixel((x+pc,y+pc))
                    pixh=imgl.getpixel((x+pc,y))
                    pixw=imgl.getpixel((x,y+pc))
                    pixd=imgl.getpixel((x+pc,y+pc))
                    # if(not pixel_flag[y+pc][x+pc] or not pixel_flag[y][x+pc] or not pixel_flag[y+pc][x]): break
                    if( abs(pixh-mean)+abs(pixw-mean)+abs(pixd-mean)>=THRESHOLD1+(pc*LAGRER_FACTOR) 
                       or txt_pix_h<255 or txt_pix_d<255 or txt_pix_w<255 or not (pixel_flag[y+pc][x] and pixel_flag[y][x+pc] and pixel_flag[y+pc][x+pc] )):
                        break
                    else:
                        pc+=STEP2
            if(y+pc>=h or x+pc>=w): pc-=STEP2
            RGBmean=[0,0,0]
            for a in range(pc):
                for b in range(pc):
                    pixel_flag[y+a][x+b]=False
                    r,g,b=img.getpixel((x+b,y+a))
                    RGBmean[0]+=r
                    RGBmean[1]+=g
                    RGBmean[2]+=b
            if(pc>BOX_SIZE_LIM):
                RGBmean=tuple(map(lambda x: interpolate(x//(pc*pc)),RGBmean))
                res=scale(Element,sum(RGBmean)//3)
                TXT2.append(txt(
                    res,
                    current_folder(r"txt\Pistilli-Roman.otf"),
                    (x,y,x+pc,y+pc),
                    RGBmean
                ))

# canvas_img=Image.new(mode="RGB",size=(w*ENLARGE,h*ENLARGE),color=(0,0,0))
# canvas=ImageDraw.Draw(canvas_img)
for todo in TXT2:
    todo.draw(ENLARGE,canvas,canvas_img)
    # print(todo.text)

print("show 2")
# canvas_img.show()
canvas_img.save(current_folder(r"style\_res3.png"))