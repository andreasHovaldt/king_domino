import cv2
import numpy as np
import os
import csv
import pandas as pd

field_biome_dict = []

biome_path_list = [
    "field_biome", "field_house_biome",
    "forest_biome", "forest_house_biome",
    "mine_biome",
    "ocean_biome", "ocean_house_biome",
    "plains_biome", "plains_house_biome",
    "swamp_biome", "swamp_house_biome"
]


for biome_name in biome_path_list:
    biome_path = f'King Domino dataset/sorted_biome_tiles/{biome_name}'
    biome_path_os = os.listdir(biome_path)

    current_biome_list = []

    for file_name in biome_path_os:
        #Read image
        current_tile = cv2.imread(f"{biome_path}/{file_name}")
        
        #Convert to hsv and take mean hue value
        current_tile = cv2.cvtColor(current_tile, cv2.COLOR_BGR2HSV)
        current_tile_hue_mean = np.mean(current_tile[:,:,0])

        field_biome_dict.append([current_tile_hue_mean, biome_name])
        
        current_biome_list.append(current_tile_hue_mean)
    
    print(f"Name: {biome_name}   meanVal: {np.mean(current_biome_list)}")
    
    #print(f"{file_name} -> {current_tile_hue_mean}")


data_header = ['Hue mean', 'Biome name']

#'''
with open('biome_data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(data_header)
    
    writer.writerows(field_biome_dict)
#'''


data = pd.read_csv("biome_data.csv")

#print(data.at[69,'Hue mean'])
#print(data.at[69,'Tile name'])
#print(data)


#all_data = np.c_[d1, d2]
#print(field_biome_dict)
#print(len(field_biome_dict))




