import random
import cv2
import numpy as np

from kingDominoFunctions import equalizeHistogram, segmentImage, determineBiome, computeCrowns

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



############################################### MAIN CODE ###############################################

img12 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/12.jpg")
img12copy = np.copy(img12)
img12Gray = cv2.cvtColor(img12copy, cv2.COLOR_BGR2GRAY)
img12Eq = equalizeHistogram(img12copy)

img4 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/4.jpg")
img4copy = np.copy(img4)

img20 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/20.jpg")
img20copy = np.copy(img20)

############# Loading #############
img12List = segmentImage(img12copy)
img20List = segmentImage(img20copy)

seaTile = img12List[2][4]
fieldTile = img12List[0][0]
forestTile = img12List[1][0]
plainsTile = img12List[2][0]
swampTile = img12List[4][0]
mineTile = img20List[2][0]
#testTile = img12List[2][1]


############# Blurring #############
#seaTileMedBlur = cv2.medianBlur(seaTile,99)
seaTileGausBlur = cv2.GaussianBlur(seaTile,(99,99),99)
fieldTileGausBlur = cv2.GaussianBlur(fieldTile,(99,99),99)
forestTileGausBlur = cv2.GaussianBlur(forestTile,(99,99),99)
plainsTileGausBlur = cv2.GaussianBlur(plainsTile,(99,99),99)
swampTileGausBlur = cv2.GaussianBlur(swampTile,(99,99),99)
mineTileGausBlur = cv2.GaussianBlur(mineTile,(99,99),99)
#testTileGausBlur = cv2.GaussianBlur(testTile,(99,99),99)

cv2.imwrite("C:/Users/Andreas/Desktop/blurredTiles/seaTile.png", seaTileGausBlur)
cv2.imwrite("C:/Users/Andreas/Desktop/blurredTiles/fieldTile.png", fieldTileGausBlur)
cv2.imwrite("C:/Users/Andreas/Desktop/blurredTiles/forestTile.png", forestTileGausBlur)
cv2.imwrite("C:/Users/Andreas/Desktop/blurredTiles/plainsTile.png", plainsTileGausBlur)
cv2.imwrite("C:/Users/Andreas/Desktop/blurredTiles/swampTile.png", swampTileGausBlur)
cv2.imwrite("C:/Users/Andreas/Desktop/blurredTiles/mineTile.png", mineTileGausBlur)

############# Subtract #############
#difference = cv2.subtract(seaTileGausBlur, testTileGausBlur)
#difference = cv2.subtract(testTileGausBlur, seaTileGausBlur)



#cv2.imshow("Sea tile", seaTile)
#cv2.imshow("Sea tile Med Blur", seaTileMedBlur)
#cv2.imshow("Sea tile Gaus Blur", seaTileGausBlur)
#cv2.imshow("Test tile Gaus Blur", testTileGausBlur)
#cv2.imshow("Difference", difference)
#cv2.waitKey()
#cv2.destroyAllWindows()
            








#kingdom12 = kingdom(img12copy)
#kingdom12.tile(2,2)
#kingdom12.showTile
#cv2.imshow("Window", kingdom12.list[4][2])

#cv2.waitKey(0)
#cv2.destroyAllWindows()



