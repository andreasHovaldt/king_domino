import cv2
import numpy as np

from imutils.object_detection import non_max_suppression
from kingDominoFunctions import writeBiomeText, segmentImage, determineBiome

###---------------------------- Classes ----------------------------###
class kingdom:
    '''
    General functions:\n
    * showImage() -> Displays board image
    * getPoints() -> (Not operational) Calculate points
    \n
    Biome functions:\n
    * biomeImage() -> Returns board image with biomes written on tiles
    * biomeImageShow() -> Displays board image with biomes written on tiles
    * biomeArray() -> Returns 5x5 NDArray with biomes corresponding to tile layout on board
    \n
    Crown functions:\n
    * countCrowns() -> Counts crowns and returns amount as an [int]
    * drawCrowns() -> Returns image with drawn crowns
    '''
    
    def __init__(self, image, crown_template_list, crown_treshold):
        self.image = image
        self.tile_array = segmentImage(image)

        #-- Crown detection --#
        self.boxes = []
        self.crown_template_list = crown_template_list
        self.crown_treshold = crown_treshold
    
    def showImage(self, pause=True):
        '''Displays board image'''
        cv2.imshow("board image", self.image)
        if pause == True:
            cv2.waitKey()
            cv2.destroyAllWindows()
    
    def getPoints(self):
        #Calculate points
        pass
    
    ###---------------------------- Biome prediction ----------------------------###
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

        
    ###---------------------------- Crown detection ----------------------------###
    
    def __detectCrown(self, image):
        '''
        !! Private method, cannot be called outside of class !!\n
        Searches image for crowns using the templates given in a list
        '''
        boxes = []
        template_list = self.crown_template_list
        
        # For loop goes through all templates in the template list
        for i in range(len(template_list)):
            # Sets the current template
            current_template = template_list[i]
            

            # First the template is rotated to fit all the possible orientations and saved to a variable
            t1 = current_template
            t2 = cv2.rotate(t1,cv2.ROTATE_90_CLOCKWISE)
            t3 = cv2.rotate(t2,cv2.ROTATE_90_CLOCKWISE)
            t4 = cv2.rotate(t3,cv2.ROTATE_90_CLOCKWISE)

            # the rotated templates are saved in an array
            template_array=[t1,t2,t3,t4]


            for i in range(len(template_array)):
                # the built in template matching function is used
                res1 = cv2.matchTemplate(np.copy(image),template_array[i],cv2.TM_CCOEFF_NORMED)

                # the x,y position for where the result is higher than the threshold is saved
                (y_points,x_points) = np.where(res1 >= self.crown_treshold)

                # the width and the height of the template is saved, to be used to determine the size of the rectangles
                w, h = template_array[i].shape[:2]

                # following for loop saves x,y-position as a tuple and iterates through the list of positions and appends boxes correlating to each position
                for(x,y) in zip(x_points, y_points):
                    boxes.append((x, y, x+w, y+h))
        
        # Uses non_max_supression on crown boxes to avoid detecting the same crown multiple times
        boxes = non_max_suppression(np.array(boxes))
        return boxes
        

    def countCrownsFull(self, reset_boxes=False):
        '''
        Counts crowns and returns amount as an [int]
        '''
        # Used if you want to re-compute amount of crowns
        if reset_boxes == True:
            self.boxes = []
        
        # Runs detectCrown() function to find crowns, only if it has not been run before
        if len(self.boxes) == 0:
            self.boxes = self.__detectCrown(self.image)
        
        # Returns number of detected crowns
        return len(self.boxes)
    
    
    def countCrownsTile(self, tile):
        '''
        Counts crowns of given tile and returns amount as an [int]
        '''
        # Runs detectCrown() function to find crowns
        boxes = self.__detectCrown(tile)
        
        # Returns number of detected crowns
        return len(boxes)
    
    
    def crownArray(self):
        '''Returns 5x5 array with biomes corresponding to crown layout on board'''
        tiles = self.tile_array
        
        # Create empty np array with same width and height dimensions as tile array 
        crown_np_array = np.zeros((tiles.shape[:2]))
        
        for y in range(tiles.shape[0]):
            for x in range(tiles.shape[1]):
                # Set current tile
                current_tile = tiles[y,x]
                # Count crowns of tiles
                crown_num = self.countCrownsTile(current_tile)
                # Set crown number in np array
                crown_np_array[y,x] = crown_num
        
        return crown_np_array
    
    
    def drawCrowns(self, image, reset_boxes=False):
        '''
        Draws rectangles around all crowns\n
        Returns image with drawn crowns
        '''
        # Used if you want to re-compute amount of crowns
        if reset_boxes == True:
            self.boxes = []
        
        # Runs detectCrown() function to find crowns, only if it has not been run before
        if len(self.boxes) == 0:
            self.__detectCrown(self.image)
        
        # Draws rectangles on the image corresponding to the crowns
        crown_image = np.copy(image)
        for(x1,y1,x2,y2) in self.boxes:
            crown_image = cv2.rectangle(np.copy(crown_image), (x1,y1),(x2,y2),(255,0,0),3)
        
        # Returns image of board with highlighted crowns
        return crown_image
    
    
    


class CrownDetect:
    '''
    Crown functions:\n
    * countCrowns()
    * drawCrowns()
    '''
    
    def __init__(self, image, crown_template_list, crown_treshold):
        '''
        image: Image of board
        crown_template_list: List of crown templates used for template matching 
        crown_threshold: Sensitivity of template matching for crown detection, higher = stricter
        '''
        
        self.image = image
        
        self.boxes = []
        self.crown_template_list = crown_template_list
        self.crown_treshold = crown_treshold
    
    
    # Function uses template matching to find crowns on self.image
    def __detectCrown(self):
        '''
        !! Private method, cannot be called outside of class !!\n
        Searches image for crowns using the templates given in a list
        '''
        template_list = self.crown_template_list
        
        # For loop goes through all templates in the template list
        for i in range(len(template_list)):
            # Sets the current template
            current_template = template_list[i]
            

            # First the template is rotated to fit all the possible orientations and saved to a variable
            t1 = current_template
            t2 = cv2.rotate(t1,cv2.ROTATE_90_CLOCKWISE)
            t3 = cv2.rotate(t2,cv2.ROTATE_90_CLOCKWISE)
            t4 = cv2.rotate(t3,cv2.ROTATE_90_CLOCKWISE)

            # the rotated templates are saved in an array
            template_array=[t1,t2,t3,t4]


            for i in range(len(template_array)):
                # the built in template matching function is used
                res1 = cv2.matchTemplate(np.copy(self.image),template_array[i],cv2.TM_CCOEFF_NORMED)

                # the x,y position for where the result is higher than the threshold is saved
                (y_points,x_points) = np.where(res1 >= self.crown_treshold)

                # the width and the height of the template is saved, to be used to determine the size of the rectangles
                w, h = template_array[i].shape[:2]

                # following for loop saves x,y-position as a tuple and iterates through the list of positions and appends boxes correlating to each position
                for(x,y) in zip(x_points, y_points):
                    self.boxes.append((x, y, x+w, y+h))
        
        # Uses non_max_supression on crown boxes to avoid detecting the same crown multiple times
        self.boxes = non_max_suppression(np.array(self.boxes))
        

    def countCrowns(self):
        # Runs detectCrown() function to find crowns, only if it has not been run before
        if len(self.boxes) == 0:
            self.__detectCrown()
        
        # Returns number of detected crowns
        self.hello = 'hello!'
        return len(self.boxes)
    
    
    def drawCrowns(self):
        # Runs detectCrown() function to find crowns, only if it has not been run before
        if len(self.boxes) == 0:
            self.__detectCrown()
        
        # Draws rectangles on the image corresponding to the crowns
        crown_image = np.copy(self.image)
        for(x1,y1,x2,y2) in self.boxes:
            crown_image = cv2.rectangle(np.copy(crown_image), (x1,y1),(x2,y2),(255,0,0),3)
        
        # Returns image of board with highlighted crowns
        return crown_image