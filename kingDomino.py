import cv2
from kingDominoClasses import kingdom, CrownDetect
from kingDominoFunctions import loadCrownTemplates
#from CrownDetect import CrownDetect
     
    
###---------------------------- MAIN CODE ----------------------------###
def main():
    ### Loading Whole Boards ###
    img4 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/4.jpg")
    img4 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/6.jpg")

    crown_templates = loadCrownTemplates()
   
    
    ### Define class ###
    board = kingdom(img4, crown_templates, 0.6)
    board.showImage(pause=False)
    
    
    ### Biome detection ###
    # Run class functions
    biome_image = board.biomeImage()
    #print(board.biomeArray())
    
    
    ### Crown detection ###
    # Run class functions to detect crowns and draw them on image
    print(f"The board contains {board.countCrowns()} crowns")
    crownImg = board.drawCrowns(biome_image)
    cv2.imshow('Board', crownImg)
    
    
    
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    



if __name__ == "__main__":
    main()



# look into this: https://techvidvan.com/tutorials/detect-objects-of-similar-color-using-opencv-in-python/






