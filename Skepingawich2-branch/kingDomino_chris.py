from unittest import result
import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
from CrownDetect_chris import CrownDetect
#import matplotlib.pyplot as plt

boxes = list()

#following function is used to slice the board into pieces and store them in the slice list
def slicing(frame):

    sliceList = []

    #extract the sice of the image
    height,width,channel = frame.shape

    #we know there are 25 equally sized squares and that the board itself is square allowing us to
    #to calculate the sice of a single square as following
    slice_width = int(width/5)
    slice_height = int(height/5)

    #following for loop will iterate through the squares
    for y in range(5):
        #here we append an array to the list 
        sliceList.append([])
        for x in range(5):
            #we calculate the slice itself
            square = frame[slice_height * y:slice_height*(y+1),slice_width * x:slice_width*(x+1)]

            #We append the square to a place in the list
            sliceList[y].append(square)
    return sliceList
            

#following function uses non_max_supression to avoid detecting the same crown multiple times
#afterwards it draws rectangles on the image
def drawCrown(image):
    global boxes
    boxes = non_max_suppression(np.array(boxes))

    for(x1,y1,x2,y2) in boxes:
        cv2.rectangle(image, (x1,y1),(x2,y2),(255,0,0),3)





#this function uses template matching to find the crwons          
def detectCrown(slice,template,t):

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

        #we access the global variable boxes where we will store our 
        global boxes

        #following for loop saves x,y-position as a tuple and iterates through the list of positions and appends a boxes
        #correlating to each position
        for(x,y) in zip(x_points, y_points):

            boxes.append((x,y,x+w,y+h))

    
        #we show the current template being used for matching
        cv2.imshow('curr_temp',template_array[i])

        #following line is used if the middle results of matching is to be showed
        cv2.imshow(f't{i}',res1)
        cv2.waitKey(0)
        cv2.destroyWindow(f't{i}')
        #same process as above is repeated for each 90degree rotation of the crown




#following function will be used to blur the images to a point where they are a solid colour
# Currently not used but could be helpful
def solidColour(slices, kernelSize ):

    blurList=[]
    for i in range(5):
        blurList.append([])
        for j in range(5):
           blurList[i].append(cv2.GaussianBlur(slices[i][j],(kernelSize,kernelSize),0))

    return blurList

        
    
##----------------End of function definitions---------------##


img = cv2.imread("C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/Cropped and perspective corrected boards/6.jpg")


#following line reads the templates correlating to a crown on each type of tile
swamp_template = cv2.imread('C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/crown_templates/swampCrown.jpg')
forest_template = cv2.imread('C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/crown_templates/forestCrown.jpg')
mine_template = cv2.imread('C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/crown_templates/mineCrown.jpg')
ocean_template = cv2.imread('C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/crown_templates/oceanCrown.jpg')
field_template = cv2.imread('C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/crown_templates/fieldCrown.jpg')
grass_template = cv2.imread('C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/crown_templates/plainsCrown.jpg')

# ... then package the templates into a list
templates =[swamp_template,forest_template,mine_template,ocean_template,field_template,grass_template]


sliceList = slicing(img)


cv2.imshow('fullimg', img)

cv2.waitKey(0)

#following lines run the function for each of the templates
# detectCrown(img,swamp_template,0.6)
# detectCrown(img,mine_template,0.6)
# detectCrown(img,ocean_template,0.6)
# detectCrown(img,forest_template,0.6)
# detectCrown(img,grass_template,0.7)
# detectCrown(img,field_template,0.6)


#now use the draw crown function to draw on top of the image
drawCrown(img)
#display the final image 

boxes = list()



cd = CrownDetect(boxes)


# for i in range(5):
#     boxes = list()
#     for j in range(5):
#         cd = CrownDetect(boxes)
#         cd.findCrown(sliceList[i][j],templates,0.6)
#         cv2.imshow(f'slice{i},{j}',sliceList[i][j])
#         cv2.waitKey(0)
#         boxes = list()

cd.findCrown(img,templates,0.6)

cv2.imshow("final",img)

cv2.waitKey(0)


# for i in range(5):
#     for j in range(5):
#       cv2.imshow(f"image{i},{j}",sliceList[i][j])
#       detectCrown(sliceList[i][j],template)





