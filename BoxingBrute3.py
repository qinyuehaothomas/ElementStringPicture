from os import path
import os,csv
from PIL import Image, ImageDraw,ImageFont
from random import randint,choice

# ====================================================================================================================================================
# Define Shits

def current_folder(file_name):
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    return path.join(d, file_name)

# with open(current_folder(r'txt\Element_sorted.txt'),"r") as f:
#     Element=f.read().split(',')


with open(current_folder(r"txt\element_abundance.csv")) as f:
    raw=csv.reader(f)
    field=next(raw)
    Element=[]
    for i in raw:
        if len(i):
            Element.append(i[1])
    Grp_element=[]
    cnt=2
    i=0
    while cnt<len(Element)//2:
        Grp_element.append([Element[k] for k in range(i,min(len(Element)-1,i+cnt))])
        i+=cnt
        cnt=cnt*2

    # group elements by decimal places
print(Grp_element)
# MAX_BOX_SIZE=45


# IMPORTANT!!!! TODO ALGRITHM
def map_to(l,v): # need to redo scaling algrithm
    #use size of box determine which category should the word be in
    # linear doesnt work!
    # alter should be max/val
    # categroise should be exponetial!
    # maybe ill need to play around with maths
    alter=choice(l[max(-len(l),-v//10)])
    return alter

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
    def draw(self,scale:int , canvas:ImageDraw, canvas_img:Image , fill=(-1,-1,-1) , bg:bool=False,rotate:bool=False):
        #scale
        font = ImageFont.truetype(self.font_path,self.font_size*scale)
        bbox= font.getbbox(self.text)  # Size of text w/font if rendered.
        txt_width ,txt_height = bbox[2]-bbox[0], bbox[3]-bbox[1]
        txt_l,txt_u=((scale*(self.rect[0]+self.rect[2])//2)-txt_width//2 , (scale*(self.rect[1]+self.rect[3])//2) - txt_height//2)
        try:
            if(fill[0]==-1): fill=self.fill
        except:
            pass
        rect=tuple(map(lambda x:x*scale,self.rect))
        if(bg):canvas.rectangle(rect,fill=self.fill)
        canvas.text((txt_l,txt_u), self.text, fill=fill,font=font,align="centre")

        if(rotate):
            rotation=choice([270,0,0,90])
            tmp = canvas_img.crop (rect)
            tmp = tmp.rotate (rotation, expand = 1)
            canvas_img.paste (tmp, (rect[0],rect[1]))


# ====================================================================================================================================================
#Load Shits

img=Image.open(current_folder(r"style\Face3.jpg"))
imgl=img.convert("L")
w,h=imgl.size

# ====================================================================================================================================================
# Here onward, First round of Boxxing(big boxes)


# delete pixel flag, change to a greyscale canvas
flag=Image.new(size=(w,h),color=255,mode='L')
flag_canvas=ImageDraw.Draw(flag)

ENLARGE=10
TXT=[]

print(h,w)
STEP1=1
LAGRER_FACTOR=1.2
THRESHOLD1=40

# need to double the scale of canvas !
for y in range(h):
    if y%10==0: print("row",y)
    for x in range(w):
        if( flag.getpixel((x,y))==255):
            # overlap problem
            # The starting block was not flagged, it eats into other boxes
            mean=imgl.getpixel((x,y))
            pc=0# pixel count
            # prevh,prevw,prevd=mean,mean,mean
            while(y+pc<h and x+pc<w):
                    pixh=imgl.getpixel((x+pc,y))
                    pixw=imgl.getpixel((x,y+pc))
                    pixd=imgl.getpixel((x+pc,y+pc))
                    # delete pixel flag, change to a greyscale canvas
                    if(flag.getpixel((x+pc,y+pc))!=255 or  flag.getpixel((x,y+pc))!=255 or flag.getpixel((x+pc,y))!=255): break
                    if( abs(pixh-mean)+abs(pixw-mean)+abs(pixd-mean)>=THRESHOLD1+(pc*LAGRER_FACTOR) ):
                        break
                    else:
                        # mean+=pixh+pixw+pixd
                        pc+=STEP1
            if(y+pc>=h or x+pc>=w): pc-=STEP1
            RGBmean=[0,0,0]
            for a in range(pc):
                for b in range(pc):
                    # pixel_flag[y+a][x+b]=False
                    r,g,b=img.getpixel((x+b,y+a))
                    RGBmean[0]+=r
                    RGBmean[1]+=g
                    RGBmean[2]+=b

            if(pc!=0):
                res=map_to(Grp_element,pc)
                # print(pc)
                cur_text=txt(
                    res,
                    current_folder(r"txt\Pistilli-Roman.otf"),
                    (x,y,x+pc,y+pc),
                    tuple(map(lambda x: x//(pc*pc),RGBmean))
                )
                cur_text.draw(1,flag_canvas,flag,fill=0)
                # flag.show()
                TXT.append(cur_text)
                # input(res)
# flag.show()
canvas_img=Image.new(mode="RGB",size=(w*ENLARGE,h*ENLARGE),color=(255,255,255))
canvas=ImageDraw.Draw(canvas_img)
for todo in TXT:
    todo.draw(ENLARGE,canvas,canvas_img)
    # print(todo.text)
# canvas_img.show()
canvas_img.save(current_folder(r"style\_res4.png"))
# input("cut")
print("round 1 done")