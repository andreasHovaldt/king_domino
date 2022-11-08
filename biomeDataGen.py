import cv2
import os
import csv
from dataFunctions import tile_feature_extraction, normalize_data


# Declare directory paths to training tiles
folder_path = "King Domino dataset/sorted_biome_tiles"
biome_path_list = [
    "field_biome", "field_house_biome",
    "forest_biome", "forest_house_biome",
    "mine_biome",
    "ocean_biome", "ocean_house_biome",
    "plains_biome", "plains_house_biome",
    "swamp_biome", "swamp_house_biome",
    
]


# Global list used to temporarily store feature and, later on, to create .csv data file
biome_feature_list = []


#---------------------------- Go through all training tiles and extract feature data ----------------------------#

# Loop through the different biome tile folders
for biome_name in biome_path_list:
    # Declare full path to folder with current training tiles
    biome_path = f'{folder_path}/{biome_name}'
    
    # Create list of all files in current directory
    biome_path_os = os.listdir(biome_path)

    # Loop through directory list of files
    for file_name in biome_path_os:
        # Read image
        current_tile = cv2.imread(f"{biome_path}/{file_name}")
        
        ### Feature extraction ###
        # Convert to hsv
        current_tile = cv2.cvtColor(current_tile, cv2.COLOR_BGR2HSV)
        # Pass tile to function for feature extraction
        tile_feature_dict = tile_feature_extraction(current_tile)
        
        ### Append current biome features to global list
        biome_feature_list.append([tile_feature_dict["Hue mean"], tile_feature_dict["Yellow"], 
                                   tile_feature_dict["Red"], tile_feature_dict["Green"], 
                                   tile_feature_dict["Blue"], tile_feature_dict["Saturation"], 
                                   biome_name])
    
    print(f"Processed '{biome_name}' tiles...")
print("Done processing dataset!")



#---------------------------- Create CSV file with sorted biome data, afterwards the data is normalized ----------------------------#

# Defining column names for data file
data_header = ['Hue mean', 'Yellow', 'Red', 'Green', 'Blue', 'Saturation', 'Biome name']
# Create and open .csv data file (First str is file path, Second str is 'w' for write, 'r' for read)
with open('biome_data.csv', 'w') as file:
    # Create writer object for the file being operated on
    writer = csv.writer(file)
    # Create column names in .csv data file
    writer.writerow(data_header)
    # Write tile features to columns in .csv data file
    writer.writerows(biome_feature_list)

# Normalize data
normalize_max_val = 100
normalize_data(normalize_max_val, "biome_data.csv", "biome_data_normalized.csv")


# Load biome data as data variable
#data = pd.read_csv("biome_data.csv")
#data_normalized = pd.read_csv("biome_data_normalized.csv")

