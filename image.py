#!python3
import cv2
import numpy
import pytesseract
from PIL import Image
import re

outfile = open("starting-strengths.txt", 'w')
infile = open("img-names.txt", 'r')
lines = infile.readlines()
# lines = ["37VA_8_front.png"]
image_folder = "./images"
# image_folder = "./"

box70 = (0,45,24,68)
box75 = (0,45,24,75)
box100 = (2,65,35,98)
use100 = True
use75 = False
use70 = False

custom_config_10 = r'--oem 3 --psm 10 outputbase digits'
custom_config_8 = r'--oem 3 --psm 8 outputbase digits'

rx = re.compile('\d+')

for line in lines:
    reject = False
    img_name = line.strip()
    print("Reading image: " + img_name)

    img = Image.open(f'{image_folder}/{img_name}')
    img2 = None
    if use100:
        img2 = img.crop(box100)
    elif use70:
        img2 = img.crop(box70)
    elif use75:
        img2 = img.crop(box75)
    else:
        print("Must choose one of 100/75/70")
        exit(1)

    s_10 = pytesseract.image_to_string(img2, config=custom_config_10)
    s_8 = pytesseract.image_to_string(img2, config=custom_config_8)
    # s = pytesseract.image_to_string(img, config=custom_config)
    s_10.strip()
    s_8.strip()
    match_8 = rx.match(s_8)
    match_10 = rx.match(s_10)
    ss_8 = "NONE"
    ss_10 = "NONE"
    strength = "NONE"
    default = ""
    if match_8 and match_10:
        ss_8 = match_8.group()
        ss_10 = match_10.group()
        if ss_8 == ss_10:
            strength = ss_10
        else:
            reject = True
            if int(ss_10) > 20:
                default = ss_8
            else:
                default = ss_10
    else:
        reject = True
        if match_8:
            ss_8 = match_8.group()
            default = ss_8
        elif match_10:
            ss_10 = match_10.group()
            default = ss_10

    if reject:
        print("ss_10: " + ss_10 + ", ss_8: " + ss_8 + ">> " + default + "\n")
        cv_img = cv2.cvtColor(numpy.array(img2), cv2.COLOR_RGB2BGR)
        cv2.imshow(img_name, cv_img)
        cv2.waitKey()
        cv2.destroyAllWindows()
        strength = input("enter correct strength: >> " + default + ": ")
        strength.strip()
        if strength == "":
            strength = default


    print("Found strength: " + strength + "\n")
    outfile.write(img_name + ':' + strength + "\n")

outfile.close()
infile.close()
print("SUCCESS")
