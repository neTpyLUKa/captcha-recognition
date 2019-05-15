import pytesseract
import argparse
import cv2
import os

def dist(x, y, sqrtFlag=True):
    if sqrtFlag:
        return sum((x - y) ** 2)
    else:
        return sum((x - y) ** 2) ** 0.5

WHITE = (216, 217, 219)
BLACK = (25, 26, 27)
min_dist = 23000
inFileName = "labels.txt"

ap = argparse.ArgumentParser()
ap.add_argument("-c", type=str, help="path to catalog")
args = vars(ap.parse_args())

path = args["c"]

n = 0
cor = 0

ans = dict()
'''
fileForRead = open(filename, 'r')
fileForRead.readline() == input()
'''
with open(inFileName, 'r', encoding='UTF-8') as inFile:
    for line in inFile:
        st, res = line.split(",")
        ans[st[4:]] = res[:-1].lower()

a = [0] * 3
for img in os.listdir(path):
    image = cv2.imread(path + '/' + img)
 #   a += image[0][0]
    (H, W) = image.shape[:2]
  #  copy = image.copy()
    for i in range(H):
       for j in range(W):
            d = dist(image[i][j], WHITE)
            if (d < min_dist):
           #     image[i][j] = WHITE
                for k in range(3):
                    image[i][j][k] = image[i][j][k] + int((WHITE[k] - image[i][j][k]) * (1 - (d / min_dist) ** 0.7))
            else:
              #  image[i][j] = BLACK
                for k in range(3):
                    image[i][j][k] = image[i][j][k] + int((BLACK[k] - image[i][j][k]) * (1 - (min_dist / d) ** 1.5))

    results = []

    conf = "-l eng --oem 1 --psm 6 digits"
    captcha = pytesseract.image_to_string(image, config="conf")
    results.append(((0, 0, W, H), captcha))

    results = sorted(results, key=lambda r:r[0][1])
    
    n += 1
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
        if (ans[img] != captcha):
            print("Mistake:", end="")
            print(img, ans[img], captcha)
            #if n < 10:
  #          cv2.imshow("Captcha recogntition", image)
   #         cv2.waitKey(0)
        else:
            print("Correct! ")
            cor += 1
print(n, cor / n)
