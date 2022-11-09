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
    ### Loading Whole Boards ###
    #img4 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/4.jpg")


    ### Segmenting Boards ###
    #img4List = segmentImage(img4)
    #img12List = segmentImage(img12)
    #img20List = segmentImage(img20)


    ### Create dictionary for tiles of boards ###
    #img12info = getTileInfo(img12List)
    #print(img12info[0][0]["location"])


    ############# Compute and Write Biome on Board ############# 
    def writeBiomeAndShow(board_number):
        print(f"Processing board {board_number}...")
        board = cv2.imread(f"King Domino dataset/Cropped and perspective corrected boards/{board_number}.jpg")
        board_biomes = writeBiomeText(board)
        cv2.imshow(f"board{board_number}biomes", board_biomes)
        cv2.waitKey()
        cv2.destroyAllWindows()

    writeBiomeAndShow(12)
    writeBiomeAndShow(20)
    writeBiomeAndShow(28)


# look into this: https://techvidvan.com/tutorials/detect-objects-of-similar-color-using-opencv-in-python/

if __name__ == "__main__":
    main()





