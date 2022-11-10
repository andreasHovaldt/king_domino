import cv2
from kingDominoClasses import kingdom
from CrownDetect import CrownDetect
     
    
###---------------------------- MAIN CODE ----------------------------###
def main():
    ### Loading Whole Boards ###
    img4 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/4.jpg")
    img = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/6.jpg")

    # Loading in the templates correlating to a crown on each type of tile...
    swamp_template = cv2.imread('King Domino dataset/Testing/swamp.jpg')
    forest_template = cv2.imread('King Domino dataset/Testing/forestCrown.jpg')
    mine_template = cv2.imread('King Domino dataset/Testing/mineCrown.jpg')
    ocean_template = cv2.imread('King Domino dataset/Testing/oceanCrown.jpg')
    field_template = cv2.imread('King Domino dataset/Testing/fieldCrown.jpg')
    grass_template = cv2.imread('King Domino dataset/Testing/grassCrown.jpg')
    # ... then package the templates into a list
    templates = [swamp_template,forest_template,mine_template,ocean_template,field_template,grass_template]


    
    # Display full image
    cv2.imshow('Board', img)
    cv2.waitKey(0)
    
    # Initiate class object 
    cd = CrownDetect(img,templates,0.6)

    # Run class functions to detect crowns and draw them on image
    print(cd.countCrowns())
    crownImg = cd.drawCrowns()
    cv2.imshow('Board', crownImg)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


    ##### Biome detection #####
    ### Define class
    board = kingdom(img4)
    
    ### Run class functions
    board.showImage(pause=False)
    board.biomeImageShow()
    print(board.biomeArray())



if __name__ == "__main__":
    main()



# look into this: https://techvidvan.com/tutorials/detect-objects-of-similar-color-using-opencv-in-python/






