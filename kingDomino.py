import cv2
import numpy as np

#Andreas version
#Count king domino


############### FUNCTIONS #################
def edgeDetection(image):
    #imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageBlur = cv2.GaussianBlur(image, (5,5), 2)
    imageCannyEdge = cv2.Canny(imageBlur, 50, 150)
    
    #cv2.imshow("Image Gray", imageGray)
    cv2.imshow("Image Blur", imageBlur)
    cv2.imshow("Image Canny", imageCannyEdge)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def crownDetection(image):
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    imageSaturation = imageHSV[:,:,1]
    thresh, imageCrownThresh = cv2.threshold(imageSaturation,50,255,cv2.THRESH_BINARY)
    
    cv2.imshow("Image HSV", imageHSV)
    cv2.imshow("Image Saturation", imageSaturation)
    cv2.imshow("Image crown thresh", imageCrownThresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def segmentImage(image):
    height, width, channels = image.shape
    squareHeight = int(height / 5)
    squareWidth = int(width / 5)
    
    for ySq in range(5):
        for xSq in range(5):
            square = image[squareHeight * ySq:squareHeight * (ySq+1), squareWidth * xSq:squareWidth * (xSq+1)]
            cv2.imshow(f"{xSq} x {ySq}", square)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
            

class Tile:
    def __init__(self, position, biome, crowns):
        self.position = position
        self.biome = biome
        self.crowns = crowns


############### MAIN CODE ################

img12 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/12.jpg")
img12copy = np.copy(img12)
img12Gray = cv2.cvtColor(img12copy, cv2.COLOR_BGR2GRAY)

img4 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/4.jpg")
img4copy = np.copy(img4)

segmentImage(img12copy)

#crownDetection(img12copy)

'''
img12HSV = cv2.cvtColor(img12copy, cv2.COLOR_BGR2HSV)
hue = img12HSV[:,:,0]
t, threshedHue = cv2.threshold(hue, 100,255,cv2.THRESH_BINARY)
modHSV = img12HSV
modHSV[:,:,0] = threshedHue

cv2.imshow("window", threshedHue)
cv2.imshow("window2", modHSV)
cv2.waitKey()
cv2.destroyAllWindows()
'''



'''
img12redChannel = img12copy[:,:,2]
t, water = cv2.threshold(img12redChannel, 5, 255, cv2.THRESH_BINARY)
cv2.imshow("Water", water)
cv2.waitKey(0)
#cv2.destroyAllWindows()

edgeDetection(water)
'''

'''
img12HistEq = cv2.equalizeHist(img12Gray)
cv2.imshow("Hist EQ", img12HistEq)
cv2.waitKey()
#cv2.destroyAllWindows()

edgeDetection(img12HistEq)

#img12gray2 = cv2.cvtColor(img12HSV, cv2.COLOR_HSV2)
'''

