import bs4
import csv
from os import path
import os

def current_folder(file_name):
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    return path.join(d, file_name)

with open(current_folder(r"txt\Relative_Abundace_from_Wiki.html"),'r') as f:
    soup=bs4.BeautifulSoup(f,"html.parser")

def sci_notation(num:str):
    ppm, percent=num[:-1].split("(")
    ppm=ppm.strip()

    # parts per million
    if("Ã—" not in ppm):
        ppm=ppm.replace(",","")
    else:
        ppm_val=ppm.split("Ã—")[0]
        ppm_pow=int(ppm.split("’")[1])
        ppm="0."+'0'*(ppm_pow-1)+ppm_val.replace(".","")

    # percentage
    percent=percent[:-1]
    if("Ã—" not in percent):
        percent=percent.replace(",","")
    else:
        percent_val=percent.split("Ã—")[0]
        percent_pow=int(percent.split("’")[1])
        percent="0."+'0'*(percent_pow-1)+percent_val.replace(".","")
    return (ppm,percent)

headings=["Name","Symbol","Goldschmidt classification","Abundance (ppm)","Abundace (%)"]
print(headings)
table=[]
for line in soup.find_all('tr')[1:]:
    # print(line.text)
    soup_line=[i.text for i in line.find_all('td')][1:]
    soup_line[3],soup_line[4]=sci_notation(soup_line[3])
    table.append(soup_line)

    print(soup_line)





with open(current_folder(r"txt\element_abundance.csv"), mode='w') as f:
    res = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    res.writerow(headings)
    res.writerows(table)
