import pytesseract
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", type=str, help="image path")
args = vars(ap.parse_args())

image = cv2.imread(args["i"])
(H, W) = image.shape[:2]

results = []

conf = ("-l eng --oem 1 --psm 6 digits")
captcha = pytesseract.image_to_string(image, config=conf)
results.append(((0, 0, W, H), captcha))

results = sorted(results, key=lambda r:r[0][1])

for (coords, captcha) in results:
    print(captcha)
    captcha = "".join([c if ord(c) < 128 else "" for c in captcha]).strip()
    cv2.imshow("Captcha recogntition", image)
    cv2.waitKey(0)
