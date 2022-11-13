import cv2
from kingDominoClasses import kingdom
from kingDominoFunctions import loadCrownTemplates
     
    
###---------------------------- MAIN CODE ----------------------------###
def main():
    ### Loading Whole Boards ###
    img4 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/4.jpg")
    img6 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/6.jpg")

    crown_templates = loadCrownTemplates()
   

    ### Define kingdom object for board 4 ###
    board_4 = kingdom(img4, crown_templates, 0.6)
    
    ### Show board 4 
    # board_4.showImage()
    img4_biomes = board_4.biomeImage()
    img4_analyzed = board_4.drawCrowns(img4_biomes)
    cv2.imshow("img4_analyzed", img4_analyzed)
    
    ### Get board 4 points
    print(f"Board 4 points: {board_4.getPoints()}")
    
    
    
    ### Define kingdom object for board 6 ###
    board_6 = kingdom(img6, crown_templates, 0.6)
    
    ### Show board
    # board_6.showImage()
    img6_biomes = board_6.biomeImage()
    img6_analyzed = board_6.drawCrowns(img6_biomes)
    cv2.imshow("img6_analyzed", img6_analyzed)
    
    ## Get board 6 points
    print(f"Board 6 points: {board_6.getPoints()}")



if __name__ == "__main__":
    main()