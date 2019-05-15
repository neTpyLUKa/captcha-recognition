import pytesseract
import argparse
import cv2
import os
from Tkinter import *
import tkFileDialog

n_buttons = 4

def dist(x, y, sqrtFlag=True):
    if sqrtFlag:
        return sum((x - y) ** 2)
    else:
        return sum((x - y) ** 2) ** 0.5

WHITE = (216, 217, 219)
BLACK = (25, 26, 27)
min_dist = 23000

def seg(image):
    (H, W) = image.shape[:2]
    for i in range(H):
       for j in range(W):
            d = dist(image[i][j], WHITE)
            if (d < min_dist):
                for k in range(3):
                    image[i][j][k] = image[i][j][k] + int((WHITE[k] - image[i][j][k]) * (1 - (d / min_dist) ** 0.8))
            else:
                for k in range(3):
                    image[i][j][k] = image[i][j][k] + int((BLACK[k] - image[i][j][k]) * (1 - (min_dist / d) ** 1.3))
    return image

buttons = [0 for i in range(n_buttons)]

def main():
    path = tkFileDialog.askopenfilename()
    image = cv2.imread(path)
    image = seg(image)
    (H, W) = image.shape[:2]
    results = []

    print(path)
    pic = PhotoImage(file='i.png')
    buttons[2].configure(image=pic)

    conf = "-l eng --oem 1 --psm 6 digits"
    captcha = pytesseract.image_to_string(image, config="conf")
    results.append(((0, 0, W, H), captcha))

    results = sorted(results, key=lambda r:r[0][1])

    for (coords, captcha) in results:
       # print(captcha)
        new = ""
        captcha.lower()
        for c in captcha:
            if ord('a') <= ord(c) <= ord('z') or ord('0') <= ord(c) <= ord('9'):
                new += c
            elif (c == '$'):
                new += 's'
        captcha = new
        buttons[1].configure(text=captcha)
       # print(captcha)

root = Tk()
can = Canvas(root, width=900, height=500)

buttons[0] = Button(root, command=lambda: main(), text = 'Select file', bg='white',fg="black")
buttons[0].place(x=400, y=50, w=100, h=50)
buttons[1] = Button(root, text = 'abacaba')
buttons[1].place(x=50, y=120, w=800, h=300)
buttons[2] = Button(root)
buttons[2].place(x=100, y=50, w=120, h=48)
buttons[3] = Button(root)
buttons[3].place(x=660, y=50, w=120, h=48)
pic = PhotoImage('i.png')
buttons[2].configure(image=pic)
can.pack()
root.mainloop()

