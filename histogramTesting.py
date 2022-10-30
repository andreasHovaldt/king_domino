import cv2
import numpy as np
import matplotlib.pyplot as plt
from kingDominoFunctions import *

textList = ["ocean", "field", "forest", "plains", "swamp", "mine"]
#text = 'ocean'
img_path = 'C:/Users/Andreas/Desktop/biomeAnalysis'
#savePath = 'savePath'
for text in textList:
    img = cv2.imread(f"C:/Users/Andreas/Desktop/biomeAnalysis/{text}.jpg")
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    img_hsv[:,:,2] = cv2.equalizeHist(img_hsv[:,:,2])

    img_eq = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

    cv2.imwrite(f"{img_path}/equalized/{text}EQ.png", img_eq)



    # HISTOGRAM
    hsv_hist = cv2.calcHist([img], [0], None, [256], [0,256])
    figure_hsv_hist = plt.figure("HSV Hist")
    plt.title(f"{text} - HSV")
    plt.xlabel("Hue value")
    plt.ylabel("pixel count")
    plt.plot(hsv_hist)
    plt.savefig(f"{img_path}\Histograms\hsv_{text}.png")
    #plt.show()
    plt.close()


'''
#img_eq_thresh = cv2.inRange(img_hsv[:,:,0], 50, 80)

cv2.imshow("img", img)
cv2.imshow("eq", img_eq)
#v2.imshow("eq_thresh", img_eq_thresh)
cv2.waitKey()
cv2.destroyAllWindows()
'''