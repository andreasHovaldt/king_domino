from unittest import result
import cv2
import numpy as np
import matplotlib.pyplot as plt



#followinf function is used to slice the board into pieces and store them in the slice list
def slicing(frame):

    sliceList = []

    #extract the sice of the image
    height,width,channel =frame.shape

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
            


#this function intends to use template matching            
def detectCrown(slice,template):

    result = cv2.matchTemplate(slice,template,cv2.TM_CCORR_NORMED)
    min_val,max_val,min_indx,max_indx=cv2.minMaxLoc(result)
    rescaled = abs(result[:,:]-min_val)*(255/(max_val-min_val))
    resInt = rescaled.astype(np.uint8)
    (thresh,final)= cv2.threshold(resInt,200,250,cv2.THRESH_BINARY)

    return final




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


img = cv2.imread("C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/Cropped and perspective corrected boards/4.jpg")
crown = cv2.imread("C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/Crown templates/crown.jpg")

sliceList = slicing(img)
#crowned = detectCrown(sliceList[0][1],crown)
blurList = solidColour(sliceList,99)


cv2.imshow("full board",img)
#cv2.imshow('square',sliceList[4][4])
cv2.imshow('blurred',blurList[0][0])
cv2.waitKey(0)
cv2.destroyAllWindows()

