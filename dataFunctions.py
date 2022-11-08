import cv2
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier


def get_hue_mean(img):
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return np.mean(hsv_img[:,:,0])

### Yellow sampling ###
yellow_sample = cv2.imread("King Domino dataset/color_samples/yellow_sample.jpg")
yellow_hue_mean = get_hue_mean(yellow_sample)
yellow_lower , yellow_upper = yellow_hue_mean * 0.85 , yellow_hue_mean * 1.2

### Green sampling ###
green_sample = cv2.imread("King Domino dataset/color_samples/green_sample.jpg")
green_hue_mean = get_hue_mean(green_sample)
green_lower , green_upper = green_hue_mean * 0.8 , green_hue_mean * 1.3

### Blue sampling ###
blue_sample = cv2.imread("King Domino dataset/color_samples/blue_sample.jpg")
blue_hue_mean = get_hue_mean(blue_sample)
blue_lower , blue_upper = blue_hue_mean * 0.85 , blue_hue_mean * 1.3

### Red sampling ###
red_sample = cv2.imread("King Domino dataset/color_samples/red_sample.jpg")
red_hue_mean = get_hue_mean(red_sample)
red_upper = red_hue_mean * 1.4
red_lower = 255 - red_upper


def tile_feature_extraction(tile_hsv):
    '''
    Extracts different features from tile:\n
        * Hue mean (Key: "Hue mean")\n
        * Hue color ranges (Keys: "Yellow", "Blue", "Green", "Red", and "Other")\n
        * Saturation mean (Key: "Saturation")\n
    \n
    Input: Tile image in HSV form \n
    Returns: Dict with extracted features
    
        Parameters:
            tile_hsv (mat): Tile picture in HSV format
    '''
    feature_dict = {
        'Hue mean': 0,
        'Yellow': 0,
        'Blue': 0,
        'Green': 0,
        'Red': 0,
        #'Other': 0,
        'Saturation': 0
    }

    for y in range(tile_hsv.shape[0]):
        for x in range(tile_hsv.shape[1]):
            
            # Counts pixels within yellow hue range
            if tile_hsv[y,x,0] >= yellow_lower and tile_hsv[y,x,0] <= yellow_upper:
                feature_dict["Yellow"] += 1

            # Counts pixels within green hue range
            if tile_hsv[y,x,0] >= green_lower and tile_hsv[y,x,0] <= green_upper:
                feature_dict["Green"] += 1

            # Counts pixels within blue hue range
            if tile_hsv[y,x,0] >= blue_lower and tile_hsv[y,x,0] <= blue_upper:
                feature_dict["Blue"] += 1

            # Counts pixels within red hue range
            if tile_hsv[y,x,0] >= red_lower or tile_hsv[y,x,0] <= red_upper:
                feature_dict["Red"] += 1

            # Counts pixels within no hue range
            #else:
                #feature_dict["Other"] += 1

    # Calculates hue and saturation mean
    feature_dict["Hue mean"] = np.mean(tile_hsv[:,:,0])
    feature_dict["Saturation"] = np.mean(tile_hsv[:,:,1])
    
    return feature_dict


def normalize_data(max_norm_val, data_path, output_path):
    '''
    Normalizes .CSV data to range between zero and specified maximum normilization value\n
    
        Parameters
            max_norm_val (int): Maximum normilization value
            data_path (str): Path to input data (Remember .csv filename)
            output_path (str): Path to .csv output file (Remember .csv in filename)
    '''
    # Loading data
    data = pd.read_csv(f"{data_path}")
    
    # Establish min and max values for data
    data_max = data.max(axis=0)
    data_min = data.min(axis=0)

    ## Declare list of features
    feature_list = data.columns[0:len(data.columns) - 1] # Remove last column entry since it contains biome name
    
    # Loops through each feature in our data
    for feature in feature_list:
        # Establishes max and min values for specific feature
        max_val = data_max[f'{feature}']
        min_val = data_min[f'{feature}']

        # Applies function to the specified feature collumn
        data[f'{feature}'] = data[f'{feature}'].apply(lambda x: max_norm_val/(max_val-min_val) * (x-min_val))

    data.to_csv(f"{output_path}")


biome_path_list = [
    "field_biome", "field_house_biome",
    "forest_biome", "forest_house_biome",
    "mine_biome",
    "ocean_biome", "ocean_house_biome",
    "plains_biome", "plains_house_biome",
    "swamp_biome", "swamp_house_biome"
    ]

def normalizeValue(value, max_norm_val, max_val, min_val):
        output = max_norm_val/(max_val-min_val) * (value-min_val)
        return output


def normalizeTileFeatures(tile_feature_dict, feature_list, max_norm_val, max_values, min_values):
    for feature in feature_list:
        # Establishes max and min values for specific feature
        max_val = max_values[f'{feature}']
        min_val = min_values[f'{feature}']
        
        #Normalize value for given feature
        tile_feature_dict[f'{feature}'] = normalizeValue(tile_feature_dict[f'{feature}'], max_norm_val, max_val, min_val)
    
    return tile_feature_dict


def determineBiome(tile):
    '''
    Computes the biome of given tile\n
        Parameters:
            tile (mat): Tile image[BGR]
            returns (str): Biome prediction
    '''
    # Convert tile to hsv
    tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
    
    # Extract features from tile
    features = tile_feature_extraction(tile_hsv)
    
    # Normalize features
    features_normalized = normalizeTileFeatures(features,feature_list,100,data_max,data_min)
    
    # Convert feature dict to list
    features_normalized_list = [features_normalized["Hue mean"], features_normalized["Yellow"], 
                               features_normalized["Red"], features_normalized["Green"], 
                               features_normalized["Blue"], features_normalized["Saturation"]]
    
    # Predict biome type
    biome_prediction = clf.predict([features_normalized_list])
    
    #print(biome_prediction[0])
    return biome_prediction[0]


data = pd.read_csv("biome_data.csv")
data_normalized = pd.read_csv("biome_data_normalized.csv")

data_max = data.max(axis=0)
data_min = data.min(axis=0)

feature_list = data.columns[0:len(data.columns) - 1]

### Seperate name column from data
#Seperate name from data
biome_names = data_normalized.pop('Biome name')
#Convert DataFrame type to numpy array
numpy_biome_names = biome_names.to_numpy()

### Convert data to numpy array and remove redundant first column 
numpy_feature_data = data_normalized.to_numpy()
numpy_feature_data = numpy_feature_data[:, 1:numpy_feature_data.shape[1]]

### Numpy array with feature data and biome int name in last column
combined_numpy_data = np.c_[numpy_feature_data, numpy_biome_names]


### Create classifier
k = 5
clf = KNeighborsClassifier(n_neighbors=k, weights="uniform", algorithm="brute")
clf.fit(X=numpy_feature_data, y=numpy_biome_names)


if __name__ == "__main__":
    #current_tile = cv2.imread("King Domino dataset/sorted_biome_tiles/mine_biome/3.jpg")
    #current_tile = cv2.imread("King Domino dataset/sorted_biome_tiles/plains_house_biome/3.jpg")
    #current_tile = cv2.imread("King Domino dataset/sorted_biome_tiles/forest_biome/9.jpg")
    #current_tile = cv2.imread("King Domino dataset/sorted_biome_tiles/ocean_biome/4.jpg")
    #current_tile = cv2.imread("King Domino dataset/sorted_biome_tiles/swamp_house_biome/0.jpg")
    current_tile = cv2.imread("King Domino dataset/sorted_biome_tiles/field_house_biome/1.jpg")

    current_tile = cv2.cvtColor(current_tile, cv2.COLOR_BGR2HSV)

    print(tile_feature_extraction(current_tile))
    
    print(f"Yellow  -->  mean:{yellow_hue_mean}  lower:{yellow_lower}  upper:{yellow_upper}")
    print(f"Green  -->  mean:{green_hue_mean}  lower:{green_lower}  upper:{green_upper}")
    print(f"Blue  -->  mean:{blue_hue_mean}  lower:{blue_lower}  upper:{blue_upper}")
    print(f"Red  -->  mean:{red_hue_mean}  lower:{red_lower}  upper:{red_upper}")