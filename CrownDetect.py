import cv2
import numpy as np
from imutils.object_detection import non_max_suppression

class CrownDetect:

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
        
        