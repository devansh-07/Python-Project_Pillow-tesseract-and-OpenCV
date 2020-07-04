import zipfile
import cv2 as cv
import os
import pytesseract
from PIL import Image
import math

def facesOnPage(text, text_list, path):
    for imgtxt in text_list:
        if text in imgtxt[1]:
            print('Results found for "{}" in file {}'.format(text, imgtxt[0]))
            temp_img = Image.open(path + imgtxt[0])
            cv_img = cv.imread(path+imgtxt[0])
            try:
                face_co_ord = face_cascade.detectMultiScale(cv_img, 1.35).tolist()
            except:
                print('But there were no faces in that file!')
                continue
            
            face_img = []
            
            for x, y, w, h in face_co_ord:
                i = temp_img.crop((x, y, x + w, y + h))
                i = i.resize((100, 100))
                face_img.append(i)
            
            x, y = 0, 0
            sheet = Image.new(temp_img.mode, (500, 100*math.ceil(len(face_img)/5)))
            for fc in face_img:
                sheet.paste(fc, (x, y))
                
                if x + 100 == sheet.width:
                    x, y = 0, y + 100
                else:
                    x = x + 100
            
            display(sheet)

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

with zipfile.ZipFile("small_img.zip", "r") as myzip:
    myzip.extractall("sampleImages")

path = "sampleImages/"
all_images = os.listdir(path)
text_list = []

for image in all_images:
    img = Image.open(path + image)
    text = pytesseract.image_to_string(img).split()
    text_list.append((image, set(text)))

######## Testing ########
facesOnPage("Christopher", text_list, path)
facesOnPage("Mark", text_list, path)
