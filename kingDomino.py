from unittest import result
import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
#import matplotlib.pyplot as plt

boxes = list()

#followinf function is used to slice the board into pieces and store them in the slice list
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
            


def drawCrown(image):
    global boxes
    boxes = non_max_suppression(np.array(boxes))

    for(x1,y1,x2,y2) in boxes:
        cv2.rectangle(image, (x1,y1),(x2,y2),(255,0,0),3)





#this function intends to use template matching            
def detectCrown(slice,template,t):

    #Undersøg cv.2 colour mask 

    t1 = template
    t2 = cv2.rotate(t1,cv2.ROTATE_90_CLOCKWISE)
    t3 = cv2.rotate(t2,cv2.ROTATE_90_CLOCKWISE)
    t4 = cv2.rotate(t3,cv2.ROTATE_90_CLOCKWISE)

    template_array=[t1,t2,t3,t4]
    threshold = t
    for i in range(4):

        res1 = cv2.matchTemplate(slice,template_array[i],cv2.TM_CCOEFF_NORMED)
        (y_points,x_points) = np.where( res1 >= threshold)
        
        w, h = template_array[i].shape[:2]

        global boxes

        for(x,y) in zip(x_points, y_points):

            boxes.append((x,y,x+w,y+h))

    

        cv2.imshow('curr_temp',template_array[i])
        cv2.imshow(f't{i}',res1)
        cv2.waitKey(0)
        cv2.destroyWindow(f't{i}')
        #same process as above is repeated for each 90degree rotation of the crown




#following function will be used to blur the images to a point where they are a solid colour
# implement a nested for loop to go through the entire list 
def solidColour(slices, kernelSize ):

    blurList=[]
    for i in range(5):
        blurList.append([])
        for j in range(5):
           blurList[i].append(cv2.GaussianBlur(slices[i][j],(kernelSize,kernelSize),0))

    return blurList

        
    
##----------------End of function definitions---------------##


img = cv2.imread("C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/Cropped and perspective corrected boards/9.jpg")
#crown = cv2.imread("C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/Crown templates/crown.jpg")
farmTile_withCrown = cv2.imread("C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/Testing/farm.jpg")
swamp_template = cv2.imread('C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/testing/swamp.jpg')
forest_template = cv2.imread('C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/testing/forestCrown.jpg')
mine_template = cv2.imread('C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/testing/mineCrown.jpg')
ocean_template = cv2.imread('C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/testing/oceanCrown.jpg')
field_template = cv2.imread('C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/testing/fieldCrown.jpg')
grass_template = cv2.imread('C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/testing/grassCrown.jpg')



#imgEq = cv2.equalizeHist(img)
# temp_eq = cv2.equalizeHist(template)

sliceList = slicing(img)
#crowned = detectCrown(sliceList[0][1],crown)
#blurList = solidColour(sliceList,3)

#blurTemplate = cv2.GaussianBlur(template,(9,9),0)


#potential way of comparing our tiles
#difference = cv2.subtract(blurList[0][0],blurTile)

#cv2.imshow('blurTemp',template)
cv2.imshow('fullimg', img)

cv2.waitKey(0)
detectCrown(img,swamp_template,0.6)
detectCrown(img,mine_template,0.6)
detectCrown(img,ocean_template,0.6)
detectCrown(img,forest_template,0.6)
detectCrown(img,grass_template,0.6)
detectCrown(img,field_template,0.6)



drawCrown(img)
cv2.imshow('finalImage',img)
cv2.waitKey(0)


# for i in range(5):
#     for j in range(5):
#       cv2.imshow(f"image{i},{j}",sliceList[i][j])
#       detectCrown(sliceList[i][j],template)





##---------------show images------------"



# cv2.imshow('square',difference)
# cv2.imshow('blurred',blurList[0][0])
# cv2.waitKey(0)
# cv2.destroyAllWindows()

