import random
import cv2
import numpy as np

from kingDominoFunctions import segmentImage

#Andreas version
#Count king domino


############################################### FUNCTIONS ###############################################
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


#Compute biome of tile
def determineBiome():
    #print("Determining biome...")
    return random.choice(["Plains", "Forest", "Swamp", "Ocean", "Wheat", "Mine"])
    

#Compute amount of crowns on tile
def computeCrowns():
    #print("Computing crowns...")
    return random.randrange(0,3,1)


            

class kingdom:
    def __init__(self, image):
        self.list = segmentImage(image)
        #self.tile = dominoTile(self.list)
        for tileY in range(5):
            for tileX in range(5):
                #setattr(self, f"tile{tileY}x{tileX}", dominoTile(self.list[tileY][tileX]))
                setattr(self, f"tile{tileY}x{tileX}", dominoTile(self.list[tileY][tileX]))
                #self.f"tile{tileY}x{tileX}" = dominoTile(self.list[tileY][tileX])
    
    #for tileY in range(5):
    #    for tileX in range(5):
            #self.globals()[]
    #        pass
    
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

img4 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/4.jpg")
img4copy = np.copy(img4)

'''
for i in range(5):
    globals()[f"n{i}"] = i
'''


img12Kingdom = kingdom(img12copy)
#print(img12Kingdom.tile0x0)
img12Kingdom.tile0x0

'''
img12List = segmentImage(img12copy)
tileClassTest = dominoTile(img12List[2][2])
print(tileClassTest)
tileClassTest.showTile()
#cv2.imshow("window2", img12List[2][2])
'''

#kingdom12 = kingdom(img12copy)
#kingdom12.tile(2,2)
#kingdom12.showTile
#cv2.imshow("Window", kingdom12.list[4][2])

#cv2.waitKey(0)
#cv2.destroyAllWindows()


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





#img12gray2 = cv2.cvtColor(img12HSV, cv2.COLOR_HSV2)


