import random
import cv2
import numpy as np

from kingDominoFunctions import equalizeHistogram, getTileInfo, segmentImage, determineBiome, computeCrowns

#Andreas version
#Count king domino


############################################### FUNCTIONS & CLASSES ###############################################
class kingdom:
    def __init__(self, image):
        self.list = segmentImage(image)
        
        #self.tile = dominoTile(self.list)
        '''
        for tileY in range(5):
            for tileX in range(5):
                #setattr(self, f"tile{tileY}x{tileX}", dominoTile(self.list[tileY][tileX]))
                setattr(self, f"tile{tileY}x{tileX}", dominoTile(self.list[tileY][tileX]))
                #self.f"tile{tileY}x{tileX}" = dominoTile(self.list[tileY][tileX])
        '''
    
    
    def tile(self, yPos, xPos):
        dominoTile(self.list[yPos][xPos])
    
    
    def getPoints(self):
        #Calculate points
        pass
    

    
class dominoTile:
    def __init__(self, tile):
        self.tile = tile
        self.biome = determineBiome()
        self.crowns = computeCrowns()
    
    def __str__(self):
        return f"Biome: {self.biome} (Crowns: {self.crowns})"
    
    def showTile(self):
        cv2.imshow("Window", self.tile)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    

#Create tileBoard with dominoTile class
def tileBoard(image, y=5, x=5):
    for ySquare in range(y):
        for xSquare in range(x):
            pass


def writeBlurBoard(boardList):
    for x in range(5):
        for y in range(5):
            tileBlur = cv2.GaussianBlur(boardList[y][x],(99,99),99)
            cv2.imwrite(f"C:/Users/Andreas/Desktop/blurredBoard/{y}x{x}.png", tileBlur)



############################################### MAIN CODE ###############################################

############# Loading Whole Boards #############
img12 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/12.jpg")

img12eq = equalizeHistogram(img12)
img12copy = np.copy(img12eq)
#img12HSV = cv2.cvtColor(img12, cv2.COLOR_BGR2HSV)
#img12copy = np.copy(img12HSV)


img4 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/4.jpg")
img4copy = np.copy(img4)

img20 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/20.jpg")
img20copy = np.copy(img20)


############# Segmenting Boards #############
img4List = segmentImage(img4copy)
img12List = segmentImage(img12copy)
img20List = segmentImage(img20copy)


############# Create dictionary for tiles of boards #############
#img12info = getTileInfo(img12List)
#print(img12info[0][0]["location"])


writeBlurBoard(img12List)

img12biomeTest, img12biomeMeanList = determineBiome(img12List[0][1])
print(img12biomeMeanList)
print(img12biomeTest)

'''
meanTile = plainsTileBlur
print(f"0 = {np.mean(meanTile[:,:,0])}  1 = {np.mean(meanTile[:,:,1])}  2 = {np.mean(meanTile[:,:,2])}")
print(np.mean(meanTile))
'''






############# Blurring #############
#seaTileMedBlur = cv2.medianBlur(seaTile,99)
#testTileGausBlur = cv2.GaussianBlur(testTile,(99,99),99)



############# Subtract #############
#difference = cv2.subtract(seaTileGausBlur, testTileGausBlur)
#difference = cv2.subtract(testTileGausBlur, seaTileGausBlur)

            








#kingdom12 = kingdom(img12copy)
#kingdom12.tile(2,2)
#kingdom12.showTile
#cv2.imshow("Window", kingdom12.list[4][2])

#cv2.waitKey(0)
#cv2.destroyAllWindows()



