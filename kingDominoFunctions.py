import cv2
import numpy as np
import random
from dataFunctions import determineBiome

############# Functions #############

#Show edges on image using canny method
def edgeDetection(image):
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageBlur = cv2.GaussianBlur(imageGray, (5,5), 2)
    imageCannyEdge = cv2.Canny(imageBlur, 50, 150)
    
    #cv2.imshow("Image Gray", imageGray)
    #cv2.imshow("Image Blur", imageBlur)
    return imageCannyEdge

#Detect crowns on image (Legacy)
def crownDetection(image):
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    imageSaturation = imageHSV[:,:,1]
    thresh, imageCrownThresh = cv2.threshold(imageSaturation,127,255,cv2.THRESH_BINARY)
    
    cv2.imshow("Image HSV", imageHSV)
    cv2.imshow("Image Saturation", imageSaturation)
    cv2.imshow("Image crown thresh", imageCrownThresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#Compute amount of crowns on tile (Legacy)
def computeCrowns(tile):
    tileThing = tile #temporary code
    #print("Computing crowns...")
    return random.randrange(0,3,1)


def equalizeHistogram(image):
    '''
    Equalize histogram of image-like type, either pass greyscale or BGR color image to function \n
    Returns equalized image
    '''
    if (len(image.shape) < 3):
        imageOutput = cv2.equalizeHist(imageOutput)
    
    elif (len(image.shape) == 3):
        imageOutput = np.copy(image)
        imageOutput = cv2.cvtColor(imageOutput, cv2.COLOR_BGR2HSV)
        imageOutput[:,:,2] = cv2.equalizeHist(imageOutput[:,:,2])
        imageOutput = cv2.cvtColor(imageOutput, cv2.COLOR_HSV2BGR)
    
    return imageOutput


def segmentImage(image):
    '''
    Segment board into 25 tiles (5x5) \n
    Returns list with tiles (Indexed by [Y][X])
    '''
    height, width, _ = image.shape
    squareHeight = int(height / 5)
    squareWidth = int(width / 5)
    
    #Create list which will be used to store the slices
    sliceList = []
    
    #For loop iterates through the squares of the image
    for y in range(5):
        
        sliceList.append([])
        
        for x in range(5):
            #Compute the slice
            square = image[squareHeight * y:squareHeight * (y+1), squareWidth * x:squareWidth * (x+1)]
            
            #Append the slice to its location in sliceList 
            sliceList[y].append(square)
    
    return sliceList


def getTileInfo (segmentList):
    '''
    Create dictionary with info for each tile of provided board
    '''
    tileInfoList = []

    for y in range(5):
        
            tileInfoList.append([])
        
            for x in range(5):
                biome = determineBiome(segmentList[y][x])
                crowns = computeCrowns(segmentList[y][x])
                
                tileInfoList[y].append({"location":[y,x], "biome":biome, "crowns":crowns})
    
    return tileInfoList
   
#Computes biomes of board image and displays it on board image 
def writeBiomeText(boardImage):
    height, width, _ = boardImage.shape
    squareHeight = int(height / 5)
    squareWidth = int(width / 5)
    
    #Segment whole board into tiles
    boardImageList = segmentImage(boardImage)
    
    #For loop goes through each tile, computes the biome, then writes it on the tile of board image
    for y in range(5):
        for x in range(5):
            biome = determineBiome(boardImageList[y][x])
            
            #cv2.putText(image, text, postion(x,y), font, fontscale, color, thicc)
            outputImage = cv2.putText(boardImage, biome, ((squareHeight * x)+10, (squareWidth * y)+10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1)
    
    #returns the original board image with biome text on each tile 
    return outputImage

