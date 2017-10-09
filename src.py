import urllib
from urllib.request import urlopen
import cv2
import numpy as np

rows = 1280
cols = 720
url='http://192.168.0.35:8080/shot.jpg'
img_back = cv2.imread('background.jpg')
background = img_back[0:cols, 0:rows ]
a = 0
limite = 40;
#painel
panel = np.zeros([100, 700, 3], np.uint8)
cv2.namedWindow("panel")

def nothing(x):
    pass

cv2.createTrackbar("L - h", "panel", 0, 179, nothing)
cv2.createTrackbar("U - h", "panel", 179, 179, nothing)

cv2.createTrackbar("L - s", "panel", 0, 255, nothing)
cv2.createTrackbar("U - s", "panel", 255, 255, nothing)

cv2.createTrackbar("L - v", "panel", 0, 255, nothing)
cv2.createTrackbar("U - v", "panel", 255, 255, nothing)


while True:
    imgResp=urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    frame=cv2.imdecode(imgNp,-1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L - h", "panel")
    u_h = cv2.getTrackbarPos("U - h", "panel")
    l_s = cv2.getTrackbarPos("L - s", "panel")
    u_s = cv2.getTrackbarPos("U - s", "panel")
    l_v = cv2.getTrackbarPos("L - v", "panel")
    u_v = cv2.getTrackbarPos("U - v", "panel")

    lower_green = np.array([l_h, l_s, l_v])
    upper_green = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask_inv = cv2.bitwise_not(mask)

    bg = cv2.bitwise_and(frame, frame, mask=mask)
    fg = cv2.bitwise_and(frame, frame, mask=mask_inv)

    fg = fg[0:cols, 0:rows]
    outputImage = np.where(fg == (0, 0, 0), (background), (fg))
    # all the opencv processing is done here
    cv2.imshow('frame', frame)
    cv2.imshow('outputImage', outputImage)
    cv2.imshow('panel', panel)
    if ord('q')==cv2.waitKey(10):
        exit(0)
