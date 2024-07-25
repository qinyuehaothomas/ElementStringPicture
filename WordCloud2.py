from os import path
import os,csv
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def current_folder(file_name):
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    return path.join(d, file_name)


# with open(current_folder(r'txt\Element_sorted.txt'),"r") as f:
#     Element=f.read().split(',')

raw_Abundance=csv.reader(open(current_folder(r"txt\element_abundance.csv")))
# print(raw_Abundance)
Element={}
fields=next(raw_Abundance)
for row in raw_Abundance:
    if(len(row)): Element[row[1]]=max(int(float(row[4])*10),1)



# filter idea
# https://www.youtube.com/watch?v=IquU5qpUOEU

from wordcloud import WordCloud, ImageColorGenerator

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# Read the whole text.
# text = open(current_folder(r"txt\Element_sorted.txt")).read()
img=Image.open(path.join(d, r"style\Face.jpg"))
w,h=img.size
FACTOR=3
img=img.resize((w*FACTOR,h*FACTOR))
coloring = np.array(img)

# relative_scaling : float (default=.5)
#     Importance of relative word frequencies for font-size.  With
#     relative_scaling=0, only word-ranks are considered.  With
#     relative_scaling=1, a word that is twice as frequent will have twice
#     the size.  If you want to consider the word frequencies and not only
#     their rank, relative_scaling around .5 often looks good.

wc = WordCloud(font_path=current_folder(r"txt\Pistilli-Roman.otf"),background_color="white",
               width=w*FACTOR,height=h*FACTOR,
            #    mask=coloring,
               max_words=4000,contour_color="black",contour_width=2,
               repeat=True,
               relative_scaling=0.01,min_font_size=4,
               max_font_size=80, random_state=42,scale=5)
# generate word cloud               
wc.generate_from_frequencies(Element)
image_colors = ImageColorGenerator(coloring)
wc.recolor(color_func=image_colors)

wc.to_file(current_folder(r"style\_res1.png"))
# create coloring from image

