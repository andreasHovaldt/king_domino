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
    


############################################### MAIN CODE ###############################################

img12 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/12.jpg")
img12copy = np.copy(img12)
img12Gray = cv2.cvtColor(img12copy, cv2.COLOR_BGR2GRAY)
img12Eq = equalizeHistogram(img12copy)

img4 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/4.jpg")
img4copy = np.copy(img4)


#Create tileBoard with dominoTile class
def tileBoard(image, y=5, x=5):
    for ySquare in range(y):
        for xSquare in range(x):
            pass
            








#kingdom12 = kingdom(img12copy)
#kingdom12.tile(2,2)
#kingdom12.showTile
#cv2.imshow("Window", kingdom12.list[4][2])

#cv2.waitKey(0)
#cv2.destroyAllWindows()



