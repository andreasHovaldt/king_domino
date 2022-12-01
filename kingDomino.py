import cv2
from kingDominoClasses import kingdom
     
    
###---------------------------- MAIN CODE ----------------------------###
def main():
    
    ### Loading Whole Boards ###
    img = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/2.jpg")

    ### Define kingdom object for board ###
    board = kingdom(img)
    
    ### Get board points
    print(f"Board points: {board.getPoints()}")
    
    ### Show board
    board.showAnalyzedBoard(pause=True)
    



def crownPrecision():
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