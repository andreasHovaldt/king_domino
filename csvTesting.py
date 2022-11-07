import pandas as pd
import numpy as np


if __name__ == "__main__":
    '''
    ####### Normalizes feature values #######
    # Maxmimum value after normalization
    max_norm_val = 1000

    # Loading data
    data = pd.read_csv("biome_data.csv")

    # Establish min and max values for data
    data_min = data.min(axis=0)
    data_max = data.max(axis=0)

    ## Declare list of features
    # New method
    feature_list = data.columns[0:len(data.columns) - 1] # Remove last column entry since it contains biome name

    # Old method
    #feature_list = [
    #    'Hue mean',
    #    'Yellow',
    #    'Red',
    #    'Green',
    #    'Blue',
    #    'Saturation']


    # Loops through each feature in our data
    for feature in feature_list:
        # Establishes max and min values for specific feature
        max_val = data_max[f'{feature}']
        min_val = data_min[f'{feature}']

        # Applies function to the specified feature collumn
        data[f'{feature}'] = data[f'{feature}'].apply(lambda x: max_norm_val/(max_val-min_val) * (x-min_val))

    data.to_csv("biome_data_normalized.csv")
    '''
    
    
    a, b = 1*3 , 2*6
    
    print(f"{a} and {b}")
    