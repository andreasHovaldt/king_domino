import random
import cv2
import numpy as np

from kingDominoFunctions import writeBiomeText, equalizeHistogram, getTileInfo, segmentImage, determineBiome, computeCrowns

#Andreas version
#Count king domino


############################################### FUNCTIONS & CLASSES ###############################################
class kingdom:
    def __init__(self, image):
        self.list = segmentImage(image)
    
    
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

#Write image of each tile in given board list to the given path
def writeBlurBoard(boardList, pathStr):
    userInput = input(f"Write board tiles to {pathStr}? [y/n]: ")
    
    if (userInput == "y"):
        for x in range(5):
            for y in range(5):
                tileBlur = cv2.GaussianBlur(boardList[y][x],(99,99),99)
                cv2.imwrite(f"{pathStr}/{y}x{x}.png", tileBlur)
        print("Board write done!")
    
    elif (userInput == "n"):
        print("Board write cancelled!")
    
    else:
        print("Unidentified response, trying again...")
        writeBlurBoard(boardList, pathStr)
    



############################################### MAIN CODE ###############################################
def main():
    pass

if __name__ == "__main__":
    main()


############# Loading Whole Boards #############
img4 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/4.jpg")
img4eq = equalizeHistogram(img4)

img12 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/12.jpg")
img12eq = equalizeHistogram(img12)

img20 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/20.jpg")
img20eq = equalizeHistogram(img20)

img26 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/26.jpg")
img26eq = equalizeHistogram(img26)


############# Segmenting Boards #############
img4List = segmentImage(img4eq)
img12List = segmentImage(img12eq)
img20List = segmentImage(img20eq)


############# Create Blurred Tile #############
#tileBlur = cv2.GaussianBlur(img20List[3][0],(99,99),99)
#cv2.imwrite("C:/Users/Andreas/Documents/GitHub/king_domino/King Domino dataset/blurredTiles/mineTileEQ.png", tileBlur)

############# Create dictionary for tiles of boards #############
#img12info = getTileInfo(img12List)
#print(img12info[0][0]["location"])



#img12biomeTest, img12biomeMeanList = determineBiome(img12List[0][3])
#print(img12biomeMeanList)
#print(img12biomeTest)


boardBiomesWithText = writeBiomeText(img26eq)
cv2.imshow("Board with biome text", boardBiomesWithText)
cv2.waitKey()
cv2.destroyAllWindows()


'''
textTest = cv2.putText(img12List[0][3], "BiomeT", (10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2) #image, text, postion(x,y), font, fontscale, color, thicc
cv2.imshow("text", textTest)
cv2.waitKey()
cv2.destroyAllWindows()
'''

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