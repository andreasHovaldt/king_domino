import cv2
import numpy as np
import random


############# Loading Reference Blurred Tiles #############
#Used for determineBiome()
'''
#Non equalized
seaTileBlur = cv2.imread("King Domino dataset/blurredTiles/seaTile.png")
fieldTileBlur = cv2.imread("King Domino dataset/blurredTiles/fieldTile.png")
forestTileBlur = cv2.imread("King Domino dataset/blurredTiles/forestTile.png")
plainsTileBlur = cv2.imread("King Domino dataset/blurredTiles/plainsTile.png")
swampTileBlur = cv2.imread("King Domino dataset/blurredTiles/swampTile.png")
mineTileBlur = cv2.imread("King Domino dataset/blurredTiles/mineTile.png")
'''

#Equalized
seaTileBlur = cv2.imread("King Domino dataset/blurredTiles/seaTileEQ.png")
fieldTileBlur = cv2.imread("King Domino dataset/blurredTiles/fieldTileEQ.png")
forestTileBlur = cv2.imread("King Domino dataset/blurredTiles/forestTileEQ.png")
plainsTileBlur = cv2.imread("King Domino dataset/blurredTiles/plainsTileEQ.png")
swampTileBlur = cv2.imread("King Domino dataset/blurredTiles/swampTileEQ.png")
mineTileBlur = cv2.imread("King Domino dataset/blurredTiles/mineTileEQ.png")


############# Functions #############

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
    #The tile to compute gets blurred
    tileBlur = cv2.GaussianBlur(tile,(99,99),99)
    
    #The tile gets compared with reference tiles and afterwards the pixel mean value is extracted
    seaMean = np.mean(cv2.subtract(seaTileBlur, tileBlur)) + 25
    fieldMean = np.mean(cv2.subtract(fieldTileBlur, tileBlur))
    forestMean = np.mean(cv2.subtract(forestTileBlur, tileBlur)) + 40
    plainsMean = np.mean(cv2.subtract(plainsTileBlur, tileBlur)) + 10
    swampMean = np.mean(cv2.subtract(swampTileBlur, tileBlur))
    mineMean = np.mean(cv2.subtract(mineTileBlur, tileBlur)) + 30
    
    #A dictionary with the mean values is created
    meanList = {"seaMean": seaMean, 
                "fieldMean": fieldMean, 
                "forestMean": forestMean, 
                "plainsMean": plainsMean, 
                "swampMean": swampMean, 
                "mineMean": mineMean}
    
    #The lowest mean value is found
    meanListMin = min(meanList.values())
    
    #The lowest mean value is compared to the different dictionary values to find the corresponding biome
    if (meanList["seaMean"] == meanListMin):
        biome = "Sea"
    elif (meanList["fieldMean"] == meanListMin):
        biome = "Field"
    elif (meanList["plainsMean"] == meanListMin):
        biome = "Plains"
    elif (meanList["forestMean"] == meanListMin):
        biome = "Forest"
    elif (meanList["swampMean"] == meanListMin):
        biome = "Swamp"
    elif (meanList["mineMean"] == meanListMin):
        biome = "Mine"
    else:
        biome = "ERROR!"
        print("determineBiomeTest Error!")
    
    #The biome is returned
    return biome, meanList
    
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
            biome, _ = determineBiome(boardImageList[y][x])
            
            #cv2.putText(image, text, postion(x,y), font, fontscale, color, thicc)
            outputImage = cv2.putText(boardImage, biome, ((squareHeight * x)+10, (squareWidth * y)+25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
            #cv2.putText(img,)
    
    #returns the original board image with biome text on each tile 
    return outputImage

#Compute amount of crowns on tile
def computeCrowns(tile):
    tileThing = tile #temporary code
    #print("Computing crowns...")
    return random.randrange(0,3,1)