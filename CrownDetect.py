from unittest import result
import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
import matplotlib.pyplot as plt

class CrownDetect:

    def __init__(self, boxes):
        self.boxes = boxes

    #this function uses template matching to find the crwons          
    def detectCrown(self, slice,template,t):

        #first the template is rotated to fit all the possible orientation and saved to a variable

        t1 = template
        t2 = cv2.rotate(t1,cv2.ROTATE_90_CLOCKWISE)
        t3 = cv2.rotate(t2,cv2.ROTATE_90_CLOCKWISE)
        t4 = cv2.rotate(t3,cv2.ROTATE_90_CLOCKWISE)

        #the template variables are saved in an array
        template_array=[t1,t2,t3,t4]

        #the threshold is used to determine who sensitive the function should be to a certain template, higher value more strict with what is a match
        threshold = t


        for i in range(4):
            #the build in template matching function is used
            res1 = cv2.matchTemplate(slice,template_array[i],cv2.TM_CCOEFF_NORMED)

            #the x,y position for where the result is higher than the threshold is saved
            (y_points,x_points) = np.where( res1 >= threshold)
        
            #the width and the height of the template is saved, to be used to determine the size of the rectangles
            w, h = template_array[i].shape[:2]

            #we access the global variable boxes where we will store our boxes position
            self.boxes

            #following for loop saves x,y-position as a tuple and iterates through the list of positions and appends a boxes
            #correlating to each position
            for(x,y) in zip(x_points, y_points):

                self.boxes.append((x,y,x+w,y+h))

    
            #we show the current template being used for matching
            #cv2.imshow('curr_temp',template_array[i])

            #following line is used if the middle results of matching is to be showed
            # cv2.imshow(f't{i}',res1)
            #cv2.waitKey(0)
            # cv2.destroyWindow(f't{i}')
            #same process as above is repeated for each 90degree rotation of the crown


    def drawCrown(self,image):
        self.boxes
        self.boxes = non_max_suppression(np.array(self.boxes))

        for(x1,y1,x2,y2) in self.boxes:
            cv2.rectangle(image, (x1,y1),(x2,y2),(255,0,0),3)
        print(len(self.boxes))

    def findCrown(self,image,templates,thresh):
        for i in range(len(templates)):
            self.detectCrown(image,templates[i],thresh)
        self.drawCrown(image)
    