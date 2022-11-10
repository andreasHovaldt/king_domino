import pandas as pd
import numpy as np
import cv2
import os
from sklearn.neighbors import KNeighborsClassifier
from kingDominoFunctions import segmentImage, equalizeHistogram, tile_feature_extraction




def writeBoard(boardList, pathStr, board_num):
    userInput = input(f"Write board tiles to {pathStr}? [y/n]: ")
    
    if (userInput == "y"):
        for x in range(5):
            for y in range(5):
                cv2.imwrite(f"{pathStr}/{board_num}_{y}x{x}.jpg", boardList[y][x])
        print("Board write done!")
    
    elif (userInput == "n"):
        print("Board write cancelled!")
    
    else:
        print("Unidentified response, trying again...")
        writeBoard(boardList, pathStr, board_num)


def determineBiome(tile):
    return 'biome name'
    
def main():
    img12 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/12.jpg")
    
    
    
    
    return
    
    
    
    # ### Creating 5x5 string np.array
    # tile_array = np.zeros((5,5)) #represents segmented board
    # biome_name_list = []
    # for y in range(tile_array.shape[0]): #5
    #     biome_name_list.append([])
    #     for x in range(tile_array.shape[1]): #5
    #         biome = determineBiome(tile_array[y,x])
    #         biome_name_list[y].append(biome)
    # biome_name_nparray = np.array([biome_name_list[0], biome_name_list[1], biome_name_list[2], biome_name_list[3], biome_name_list[4]])
    # print(biome_name_nparray)
    
    
    # ### Image/board loading
    # img12 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/12.jpg")
    # img70 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/70.jpg")
    
    
    # ### Lab colorspace testing 
    # img_lab = cv2.cvtColor(img12, cv2.COLOR_BGR2Lab)
    # img_L = img_lab[:,:,0]
    # img_a = img_lab[:,:,1]
    # img_b = img_lab[:,:,2]
    
    
    # ### Equalized RGB 
    # img12_hsv = cv2.cvtColor(img12, cv2.COLOR_BGR2HSV)
    # print([np.mean(img12[:,:,0]), np.mean(img12[:,:,1]), np.mean(img12[:,:,2])])
    
    # img12_eq = equalizeHistogram(img12)
    # img70_eq = equalizeHistogram(img70)
    # cv2.imshow("img12", img12)
    # cv2.imshow("eq12", img12_eq)
    # cv2.imshow("img70", img70)
    # cv2.imshow("eq70", img70_eq)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    # #print("done")
    
    # img12_hsv_eq = cv2.cvtColor(img12_eq, cv2.COLOR_BGR2HSV)
    # #print([np.mean(img12_eq[:,:,0]), np.mean(img12_eq[:,:,1]), np.mean(img12_eq[:,:,2])])
    # print(np.mean(img12_eq))
    
    
    
    
    # ### Rename files in directory
    # folder_path = 'King Domino dataset/sorted_biome_tiles_simplified/swamp_house'
    # dir_list = os.listdir(folder_path)
    # #print(dir_list)
    # name_number = 26
    # for tile in dir_list:
    #     os.rename(f'{folder_path}/{tile}', f'{folder_path}/{name_number}.jpg')
    #     name_number += 1
    
    
    # ### Write specific tile to path
    # # Declare directory paths to training tiles
    # folder_path = "King Domino dataset/Cropped and perspective corrected boards"
    # output_path = "C:/Users/Andreas/Desktop/new_sorted_biome_tiles"
    # board_number = '68'
    # current_board = cv2.imread(f'{folder_path}/{board_number}.jpg')
    # board_list = segmentImage(current_board)
    # cv2.imwrite(f'{output_path}/unasigned_{board_number}.jpg', board_list[4][4])
    
    
    # ### Segment multiple boards and write tiles to path
    # boards_to_segment = 30
    # for board_number in range(1,(boards_to_segment*2)+1,2):
    #     # Path to board
    #     board_path = f'{folder_path}/{board_number}.jpg'
    #     current_board = cv2.imread(board_path)
    #     board_list = segmentImage(current_board)
    #     writeBoard(board_list,output_path,board_number)
    
       
    
if __name__ == "__main__":
    main()