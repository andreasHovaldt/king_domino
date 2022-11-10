from unittest import result
import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
import matplotlib.pyplot as plt

class CrownDetect:

    def __init__(self, image):
        self.boxes = []
        self.image = image
    
    
    # this function uses template matching to find the crowns          
    def detectCrown(self, template, threshold):
        '''
        Searches image for crown
        Threshold is used to determine how sensitive the function should be to a certain template, higher value more strict with what is a match
        '''
        # first the template is rotated to fit all the possible orientation and saved to a variable
        t1 = template
        t2 = cv2.rotate(t1,cv2.ROTATE_90_CLOCKWISE)
        t3 = cv2.rotate(t2,cv2.ROTATE_90_CLOCKWISE)
        t4 = cv2.rotate(t3,cv2.ROTATE_90_CLOCKWISE)

        # the rotated templates are saved in an array
        template_array=[t1,t2,t3,t4]

        
        for i in range(len(template_array)):
            # the build in template matching function is used
            res1 = cv2.matchTemplate(self.image,template_array[i],cv2.TM_CCOEFF_NORMED)

            # the x,y position for where the result is higher than the threshold is saved
            (y_points,x_points) = np.where(res1 >= threshold)
        
            # the width and the height of the template is saved, to be used to determine the size of the rectangles
            w, h = template_array[i].shape[:2]

            # following for loop saves x,y-position as a tuple and iterates through the list of positions and appends boxes correlating to each position
            for(x,y) in zip(x_points, y_points):
                self.boxes.append((x, y, x+w, y+h))


    def findCrowns(self,templates,threshold):
        for i in range(len(templates)):
            self.detectCrown(templates[i],threshold)
        
        # Uses non_max_supression on crown boxes to avoid detecting the same crown multiple times
        self.boxes = non_max_suppression(np.array(self.boxes))

        # Draws rectangles on the image corresponding to the crowns
        for(x1,y1,x2,y2) in self.boxes:
            cv2.rectangle(self.image, (x1,y1),(x2,y2),(255,0,0),3)
        
        return len(self.boxes)
    