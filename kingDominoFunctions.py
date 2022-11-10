import cv2
import numpy as np
import pandas as pd
import os
from sklearn.neighbors import KNeighborsClassifier

import random #Needs to be removed -> Used in computeCrowns() for testing


###---------------------------- kingDominoFunctions ----------------------------###

# (Legacy, un-used) Show edges on image using canny method 
def edgeDetection(image):
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageBlur = cv2.GaussianBlur(imageGray, (5,5), 2)
    imageCannyEdge = cv2.Canny(imageBlur, 50, 150)
    
    #cv2.imshow("Image Gray", imageGray)
    #cv2.imshow("Image Blur", imageBlur)
    return imageCannyEdge


def equalizeHistogram(image):
    '''
    Equalize histogram of image-like type, either pass greyscale or BGR color image to function \n
    Returns equalized image
    '''
    if (len(image.shape) < 3):
        imageOutput = cv2.equalizeHist(imageOutput)
    
    elif (len(image.shape) == 3):
        imageOutput = np.copy(image)
        imageOutput = cv2.cvtColor(imageOutput, cv2.COLOR_BGR2HSV)
        imageOutput[:,:,2] = cv2.equalizeHist(imageOutput[:,:,2])
        imageOutput = cv2.cvtColor(imageOutput, cv2.COLOR_HSV2BGR)
    
    return imageOutput


def segmentImage(image):
    '''
    Segment board into 25 tiles (5x5) \n
    Returns list with tiles (Indexed by [Y][X])
    '''
    height, width, _ = image.shape
    squareHeight = int(height / 5)
    squareWidth = int(width / 5)
    
    #Create list which will be used to store the slices
    sliceList = []
    
    #For loop iterates through the squares of the image
    for y in range(5):
        
        sliceList.append([])
        
        for x in range(5):
            #Compute the slice
            square = image[squareHeight * y:squareHeight * (y+1), squareWidth * x:squareWidth * (x+1)]
            
            #Append the slice to its location in sliceList 
            sliceList[y].append(square)
    
    #convert slice list to np.array
    sliceList_nparray = np.array([sliceList[0],sliceList[1],sliceList[2],sliceList[3],sliceList[4]])
    return sliceList_nparray


def writeBiomeText(boardImage):
    '''
    Predicts tile biomes of board and writes it on each tile
        Parameters:
            boardImage (mat): Image[BGR] of board
            Returns (mat): Image[BGR] of board with predicted tile biomes text
    '''
    height, width, _ = boardImage.shape
    squareHeight = int(height / 5)
    squareWidth = int(width / 5)
    
    #Segment whole board into tiles
    boardImageArray = segmentImage(boardImage)
    
    #For loop goes through each tile, computes the biome, then writes it on the tile of board image
    for y in range(5):
        for x in range(5):
            biome = determineBiome(boardImageArray[y,x])
            
            #cv2.putText(image, text, postion(x,y), font, fontscale, color, thicc)
            outputImage = cv2.putText(boardImage, biome, ((squareHeight * x)+10, (squareWidth * y)+10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1)
    
    #returns the original board image with biome text on each tile 
    return outputImage



###---------------------------- dataFunctions ----------------------------###

# Declaring functions for training data manipulation

def get_hue_mean(img):
    '''
    Compute HUE mean from BGR image
    
        Parameters:
            img (mat): Image[BGR]
            Returns (float): Mean value of HUE channel for image
    '''
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return np.mean(hsv_img[:,:,0])


def tile_feature_extraction(tile):
    '''
    Extracts different features from tile:\n
        * Hue mean (Key: "Hue mean")\n
        * Hue color ranges (Keys: "Yellow", "Blue", "Green", and "Red")\n
        * Saturation mean (Key: "Saturation")\n
    
        Parameters:
            tile (mat): Tile picture in BGR format
            Returns (dict): Dict with extracted features
    '''
    feature_dict = {
        'Hue mean': 0,
        'Yellow': 0,
        'Red': 0,
        'Green': 0,
        'Blue': 0,
        'Saturation': 0,
        'RedEQ': 0,
        'GreenEQ': 0,
        'BlueEQ': 0
    }

    # Convert tile to hsv and lab
    tile_hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
    tile_lab = cv2.cvtColor(tile, cv2.COLOR_BGR2Lab)
    
    
    for y in range(tile_hsv.shape[0]):
        for x in range(tile_hsv.shape[1]):
            
            # Counts pixels within yellow hue range
            if tile_hsv[y,x,0] >= yellow_lower and tile_hsv[y,x,0] <= yellow_upper:
                feature_dict["Yellow"] += 1

            # Counts pixels within red hue range
            if tile_hsv[y,x,0] >= red_lower or tile_hsv[y,x,0] <= red_upper:
                feature_dict["Red"] += 1
            
            # Counts pixels within green hue range
            if tile_hsv[y,x,0] >= green_lower and tile_hsv[y,x,0] <= green_upper:
                feature_dict["Green"] += 1

            # Counts pixels within blue hue range
            if tile_hsv[y,x,0] >= blue_lower and tile_hsv[y,x,0] <= blue_upper:
                feature_dict["Blue"] += 1

            
            # Counts pixels within lab
            

    # Calculates hue and saturation mean
    feature_dict["Hue mean"] = np.mean(tile_hsv[:,:,0])
    feature_dict["Saturation"] = np.mean(tile_hsv[:,:,1])
    
    
    # Equalize BGR image
    tile_eq = equalizeHistogram(tile)
    
    # Calculates channel means for equalized BGR image
    feature_dict["RedEQ"] = np.mean(tile_eq[:,:,2])
    feature_dict["GreenEQ"] = np.mean(tile_eq[:,:,1])
    feature_dict["BlueEQ"] = np.mean(tile_eq[:,:,0])
    
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


def normalizeValue(value, max_norm_val, max_val, min_val):
        '''
        Normalizes value from zero to given max normilization value with given max and min ranges for value
        
            Parameters:
                value(int,float): Value to normalize
                max_norm_val(int,float): Upper bound of nomilization value
                max_val(int,float): The highest possible value for 'value'
                min_val(int,float): The lowest possible value for 'value'
                Returns(float): Normalized value within ranges given
        '''
        output = max_norm_val/(max_val-min_val) * (value-min_val)
        return output


def normalizeTileFeatures(tile_feature_dict, feature_list, max_norm_val, max_values, min_values):
    '''
    Normalizes values of feature dict (Different normlization for each feature)
    '''
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
    
    # Extract features from tile
    features = tile_feature_extraction(tile)
    
    # Normalize features
    features_normalized = normalizeTileFeatures(features,feature_list,100,data_max,data_min)
    
    # Convert feature dict to list
    features_normalized_list = [features_normalized["Hue mean"], features_normalized["Yellow"], 
                               features_normalized["Red"], features_normalized["Green"], 
                               features_normalized["Blue"], features_normalized["Saturation"],
                               features_normalized["RedEQ"], features_normalized["GreenEQ"],
                               features_normalized["BlueEQ"]]
    
    # Predict biome type
    biome_prediction = clf.predict([features_normalized_list])
    
    return biome_prediction[0]


def writeBiomeAndShow(board_filename, board_directory, pause=True):
        '''
        Predicts and writes biome on each tile of board, then displays it
            Parameters:
                board_filename (str): Full file name of board
                board_directory (str): Directory path to folder with board_filename
        '''
        print(f"Processing board [{board_filename}]...")
        board = cv2.imread(f"{board_directory}/{board_filename}")
        board_biomes = writeBiomeText(board)
        cv2.imshow(f"Board [{board_filename}] with biome prediction", board_biomes)
        if pause == True:
            cv2.waitKey()
            cv2.destroyAllWindows()


def predictionPrecisionTest(board_directory='King Domino dataset/untrained_boards'):
    '''
    Goes trough all boards in given directory one at a time.\n
    Predicts and writes biome on each tile of board, then displays it.\n
    Afterwards asks for user input in terminal for amount of wrong biome predictions.\n
    When through all boards in directory, calculates and prints precision of biome predictions.\n
    Press 'ESC' to exit prematurely.
        
        Parameters:
            board_directory (str): Path to folder with boards for testing on (default='King Domino dataset/untrained_boards')
    '''
    untrained_boards_list = os.listdir(board_directory)
    wrong_predictions = 0
    correct_predictions = 0
    total_predictions = 0
    for board in untrained_boards_list:
        writeBiomeAndShow(board, board_directory, False)
        key = cv2.waitKey()
        if key == 27: # ESC
            break
        cv2.destroyAllWindows()
        userInput = input(f"How many wrong predictions? [int]: ")
        wrong_predictions += int(userInput)
        correct_predictions += 25 - int(userInput)
        total_predictions += 25
    cv2.destroyAllWindows

    print(f"Precision = {(correct_predictions/total_predictions)*100}% -> {correct_predictions}/{total_predictions}")


def loadCrownTemplates(crown_template_directory='King Domino dataset\crown_templates'):
    '''
    Loads in the crown templates and adds them to a list
    '''
    templates = []
    for template in os.listdir(crown_template_directory):
        templates.append(cv2.imread(f'King Domino dataset/crown_templates/{template}'))
    
    return templates



########### Declaring hue color samples ###########
# Used to create lower and upper bounds for specfic hue ranges corresponding to yellow, green, blue and red
# These color ranges are used for feature extraction

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


########### Loading training data and declaring training data related variables ###########
# Loading training data
data = pd.read_csv("biome_data.csv")
data_normalized = pd.read_csv("biome_data_normalized.csv")

# Declaring maximum and minimum values for data set, used for normalizing later on
data_max = data.max(axis=0)
data_min = data.min(axis=0)

# Declaring list of strings containing types of features
feature_list = data.columns[0:len(data.columns) - 1]


########### Making training data compatible with sklearn KNeighborsClassifier ###########
# To make our data compatible, it is desired to seperate our ground truths from our feature vectors.
# Thus we want an array with ground truths, and an array with feature vectors
# Note: ground truth 'n' in its array should correspond to feature vector 'n' in the feature array

# Seperate name column from data and convert 'DataFrame' type to numpy array
biome_names = data_normalized.pop('Biome name')
numpy_biome_names = biome_names.to_numpy()

# Convert data to numpy array and remove redundant first column (First column only corresponds to the index of the rows)
'''Need to look into normalization since it might be the cause of this redundant column'''
numpy_feature_data = data_normalized.to_numpy()
numpy_feature_data = numpy_feature_data[:, 1:numpy_feature_data.shape[1]]


########### Create k-nearest-neighbor classifier ###########
# No. of neighbors new tile is compared to 
k = 3
# Classifier is used for predicting new tile biomes in determineBiome() function
clf = KNeighborsClassifier(n_neighbors=k, weights="uniform", algorithm="brute")
clf.fit(X=numpy_feature_data, y=numpy_biome_names)



########### Internal testing ###########
def main():
       
    predictionPrecisionTest()


if __name__ == "__main__":
    main()


