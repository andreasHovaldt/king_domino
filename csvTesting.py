import pandas as pd
import numpy as np
import cv2

from sklearn.neighbors import KNeighborsClassifier
from dataFunctions import tile_feature_extraction

if __name__ == "__main__":
    
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
    
    
    def cvtBiomeStr2Int(name):
        '''
        LEGACY FUNCTION\n
        Turns biome name str to corresponding int
        '''
        number = 0
        for biome_name in biome_path_list:
            if name == biome_name:
                return number
            else:
                number += 1
    
    
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
        
    
    
    # Create classifier
    k = 5
    clf = KNeighborsClassifier(n_neighbors=k, weights="uniform", algorithm="brute")
    clf.fit(X=numpy_feature_data, y=numpy_biome_names)
    
    # Load test tiles
    field = cv2.imread("field_test.jpg")
    forestHouse = cv2.imread("forestHouse_test.jpg")
    mine = cv2.imread("mine_test.jpg")
    
    print(determineBiome(field))
    print(determineBiome(forestHouse))
    print(determineBiome(mine))
    
       
    
    