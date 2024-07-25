from os import path
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def current_folder(file_name):
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    return path.join(d, file_name)


with open(current_folder(r'txt\Element_sorted.txt'),"r") as f:
    Element=f.read().split(',')

def scale(l,v):
    return l[int((v/255)*len(l))]

# filter idea
# https://www.youtube.com/watch?v=IquU5qpUOEU

from wordcloud import WordCloud, ImageColorGenerator

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# Read the whole text.
text = open(current_folder(r"txt\Element_sorted.txt")).read()

alice_coloring = np.array(Image.open(path.join(d, r"style\Face.jpg")))

wc = WordCloud(background_color="white", max_words=2000, mask=alice_coloring,repeat=True,
                max_font_size=40, random_state=42,scale=10)
# generate word cloud               
wc.generate(text)
image_colors = ImageColorGenerator(alice_coloring)
wc.recolor(color_func=image_colors)
wc.to_file(current_folder(r"style\_res1.png"))
# create coloring from image

