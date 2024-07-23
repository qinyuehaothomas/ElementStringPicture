# yea you can use this to sort any string density...


# clean some files
# with open('C:\D\Projects\Periodic Table Pic\ElementStringPicture\Element.txt',"r+") as f:
#     L=[i.split(" ")[0] for i in f.readlines()]
#     print(L)
#     res=""
#     for i in L:
#         if(i!='\n'):
#             res+=i+','
#     print(res)
#     f.write(res)
from PIL import Image, ImageDraw, ImageFont
from os import path
import os

def current_folder(file_name):
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    return path.join(d, file_name)

# This is just reading files, u can replace Element with the char you want to sort
with open(current_folder(r'txt\Element.txt'),"r+") as f:
    Element=f.read().split(",")[:-1]

# These two argument need to be manually adjuested!
box=(255,255)
font_size=102

# Dont have to keep creating new img i guess?
img = Image.new('L', (box[0]*len(Element),box[1]), color=(255))
img_draw = ImageDraw.Draw(img)
thickness=[]
cnt=0
font = ImageFont.truetype(current_folder(r"txt\Pistilli-Roman.otf"), font_size)

for elem in Element:


    img_draw.rectangle((0,0,box[0],box[1]), fill ="white") 
    bbox= font.getbbox(elem)  # Size of text w/font if rendered.

    txt_width ,txt_height = bbox[2]-bbox[0], bbox[3]-bbox[1]
    tx, ty = box[0]//2 - txt_width//2, box[1]//2 - txt_height//2  # Center of text.
    img_draw.text((tx, ty), elem, fill=0, font=font, align='center')

    cur=[0,elem]
    for i in range(box[0]):
        for j in range(box[1]):
            if(img.getpixel((i,j))==0):
                cur[0]+=1
    thickness.append(cur)
    cnt+=1

# img.show()
thickness.sort(key=lambda x:x[0])
print(thickness)
with open(current_folder(r'txt\Element_sorted.txt'),"w") as f:
    f.writelines([i[1]+',' for i in thickness])

    
