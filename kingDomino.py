import cv2
from kingDominoClasses import kingdom
     
    
###---------------------------- MAIN CODE ----------------------------###
def main():
    
    # ### Loading Whole Boards ###
    # img20 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/20.jpg")
    # img6 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/6.jpg")
   

    # ### Define kingdom object for board 4 ###
    # board_20 = kingdom(img20)
    
    # ### Show board 20 
    # # board_20.showImage()
    # img20_biomes = board_20.biomeImage()
    # img20_analyzed = board_20.drawCrowns(img20_biomes)
    # cv2.imshow("img20_analyzed", img20_analyzed)
    
    # ### Get board 20 points
    # print(f"Board 20 points: {board_20.getPoints()}")

    
    # ### Define kingdom object for board 6 ###
    # board_6 = kingdom(img6)
    
    # ### Show board
    # # board_6.showImage()
    # img6_biomes = board_6.biomeImage()
    # img6_analyzed = board_6.drawCrowns(img6_biomes)
    # cv2.imshow("img6_analyzed", img6_analyzed)
    
    # ## Get board 6 points
    # print(f"Board 6 points: {board_6.getPoints()}")
    
    import os
    
    total_crowns = 0
    true_crowns = 0
    false_crowns = 0
    
    untrained_boards_list = os.listdir('King Domino dataset/untrained_boards')
    for boards in untrained_boards_list:
        img = cv2.imread(f"King Domino dataset/untrained_boards/{boards}")
    
        board = kingdom(img)
        board_crowns = board.drawCrowns(img)
        cv2.imshow(f"{boards}", board_crowns)
        cv2.waitKey()
        cv2.destroyAllWindows()
        
        total_crowns += int(input(f"total_crowns: "))
        true_crowns += int(input(f"true_crowns: "))
        false_crowns += int(input(f"false_crowns: "))
    print(f"total_crowns: {total_crowns}")
    print(f"true_crowns: {true_crowns}")
    print(f"false_crowns: {false_crowns}")
    


if __name__ == "__main__":
    main()
    cv2.waitKey()
    cv2.destroyAllWindows()