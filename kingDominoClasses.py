import cv2
import numpy as np

from kingDominoFunctions import writeBiomeText, segmentImage, determineBiome

###---------------------------- Classes ----------------------------###
class kingdom:
    def __init__(self, image):
        self.image = image
        self.tile_array = segmentImage(image)
    
    
    def showImage(self, pause=True):
        '''Displays board image'''
        cv2.imshow("board image", self.image)
        if pause == True:
            cv2.waitKey()
            cv2.destroyAllWindows()
    
    def biomeImage(self):
        '''Returns board image with biomes written on tiles'''
        biome_name_img = writeBiomeText(self.image)
        return biome_name_img
    
    def biomeImageShow(self, pause=True):
        '''Displays board image with biomes written on tiles'''
        cv2.imshow("biomeImage", self.biomeImage())
        if pause == True:
            cv2.waitKey()
            cv2.destroyAllWindows()
    
    def biomeArray(self):
        '''Returns 5x5 NDArray with biomes corresponding to tile layout on board'''
        tiles = self.tile_array
        biome_name_list = []
        
        for y in range(tiles.shape[0]): #5
            biome_name_list.append([])
            for x in range(tiles.shape[1]): #5
                biome = determineBiome(tiles[y,x])
                biome_name_list[y].append(biome)
        #Convert list with lists to numpy array
        biome_name_nparray = np.array([biome_name_list[0], biome_name_list[1], biome_name_list[2], biome_name_list[3], biome_name_list[4]])
        return biome_name_nparray
        
    def getPoints(self):
        #Calculate points
        pass