import cv2
import numpy as np
import matplotlib.pyplot as plt

#this list is going to be used to store the image slices from the board
sliceList = []

#followinf function is used to slice the board into pieces and store them in the slice list
def slicing(frame):

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
            

            



img = cv2.imread("C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/Cropped and perspective corrected boards/12.jpg")


slicing(img)

cv2.imshow("full board",img)
cv2.imshow('square',sliceList[1][0])
cv2.waitKey(0)
cv2.destroyAllWindows()

