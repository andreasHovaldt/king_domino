import cv2
import numpy as np

def edgeDetection(image):
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageBlur = cv2.GaussianBlur(imageGray, (5,5), 2)
    imageCannyEdge = cv2.Canny(imageBlur, 50, 150)
    
    cv2.imshow("Image Gray", imageGray)
    cv2.imshow("Image Blur", imageBlur)
    cv2.imshow("Image Canny", imageCannyEdge)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def crownDetection(image):
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    imageSaturation = imageHSV[:,:,1]
    thresh, imageCrownThresh = cv2.threshold(imageSaturation,127,255,cv2.THRESH_BINARY)
    
    cv2.imshow("Image HSV", imageHSV)
    cv2.imshow("Image Saturation", imageSaturation)
    cv2.imshow("Image crown thresh", imageCrownThresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def equalizeHistogram(image):
    #Needs grayscale image
    imageHistEq = cv2.equalizeHist(image)
    cv2.imshow("Hist EQ", imageHistEq)
    cv2.waitKey()
    cv2.destroyAllWindows()


def segmentImage(image):
    height, width, channels = image.shape
    squareHeight = int(height / 5)
    squareWidth = int(width / 5)
    
    #Create list which will be used to store the slices
    sliceList = []
    
    #For loop iterates through the squares of the image
    for ySq in range(5):
        
        sliceList.append([])
        
        for xSq in range(5):
            #Compute the slice
            square = image[squareHeight * ySq:squareHeight * (ySq+1), squareWidth * xSq:squareWidth * (xSq+1)]
            
            #Append the slice to its location in sliceList 
            sliceList[ySq].append(square)
    
    return sliceList