import cv2
import numpy as np
import random

#Show edges on image using canny method
def edgeDetection(image):
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageBlur = cv2.GaussianBlur(imageGray, (5,5), 2)
    imageCannyEdge = cv2.Canny(imageBlur, 50, 150)
    
    #cv2.imshow("Image Gray", imageGray)
    #cv2.imshow("Image Blur", imageBlur)
    return imageCannyEdge

#Detect crowns on image (Not operational)
def crownDetection(image):
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    imageSaturation = imageHSV[:,:,1]
    thresh, imageCrownThresh = cv2.threshold(imageSaturation,127,255,cv2.THRESH_BINARY)
    
    cv2.imshow("Image HSV", imageHSV)
    cv2.imshow("Image Saturation", imageSaturation)
    cv2.imshow("Image crown thresh", imageCrownThresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#Equalize histogram of image (Both color and greyscale images)
def equalizeHistogram(image):
    imageOutput = np.copy(image)
    if (len(image.shape) < 3):
        imageOutput = cv2.equalizeHist(imageOutput)
    
    elif (len(image.shape) == 3):
        for c in range(image.shape[2]):
            imageOutput[:,:,c] = cv2.equalizeHist(imageOutput[:,:,c])
    
    return imageOutput

#Segment board into 25 tiles (5x5)
def segmentImage(image):
    height, width, channels = image.shape
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

#Creat dictionary with info for each tile of provided board
def getTileInfo (segmentList):
    tileInfoList = []

    for y in range(5):
        
            tileInfoList.append([])
        
            for x in range(5):
                biome = determineBiome(segmentList[y][x])
                crowns = computeCrowns(segmentList[y][x])
                
                tileInfoList[y].append({"location":[y,x], "biome":biome, "crowns":crowns})
    
    return tileInfoList


#Compute biome of tile
def determineBiome(tile):
    tileThing = tile #temporary code
    #print("Determining biome...")
    return random.choice(["Plains", "Forest", "Swamp", "Ocean", "Wheat", "Mine"])
    

#Compute amount of crowns on tile
def computeCrowns(tile):
    tileThing = tile #temporary code
    #print("Computing crowns...")
    return random.randrange(0,3,1)