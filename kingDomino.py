import cv2
from kingDominoClasses import kingdom

#Count king domino

###---------------------------- MAIN CODE ----------------------------###
def main():
    ### Loading Whole Boards ###
    img4 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/4.jpg")
    
    ### Define class
    board = kingdom(img4)
    
    ### Run class functions
    board.showImage(pause=False)
    board.biomeImageShow()
    print(board.biomeArray())
    
    
    return
    

# look into this: https://techvidvan.com/tutorials/detect-objects-of-similar-color-using-opencv-in-python/

if __name__ == "__main__":
    main()





