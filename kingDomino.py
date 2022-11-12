import cv2
import numpy as np
from collections import deque
import time


from kingDominoClasses import CrownDetect, kingdom
from kingDominoFunctions import loadCrownTemplates, zipArrays

#from CrownDetect import CrownDetect

   
###---------------------------- MAIN CODE ----------------------------###
def main():
    ### Loading Whole Boards ###
    img4 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/4.jpg")
    img4 = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/6.jpg")

    crown_templates = loadCrownTemplates()
   
    
    ### Define class ###
    board = kingdom(img4, crown_templates, 0.6)
    #board.showImage(pause=False)
    
    
    ### Biome detection ###
    #Run class functions
    biome_image = board.biomeImage()
    biomeArray = board.biomeArray()

   # print(biomeArray)
    
    
    # ### Crown detection ###
    # Run class functions to detect crowns and draw them on image
    print(f"The board contains {board.countCrownsFull()} crowns")
    crownImg = board.drawCrowns(biome_image)
    cv2.imshow('Board', crownImg)
    crownArray = board.crownArray()

    print(crownArray)
    
    
    tile_and_size = list()

    possible_biomes = ['field','mine','swamp','forest','plains','ocean']
    np_arr = zipArrays(biomeArray,crownArray)
    print(np_arr) 

    output_img = np.zeros((biomeArray.shape[0],biomeArray.shape[1]), np.uint8)
    
    burn_queue = deque([])

    current_id = 1     
    output_img = np.zeros((5,5),np.uint8)

    def identifyIgnition(currentPixel,inputImage):

        #we parse the current pixel to the function
        [y,x] = currentPixel
        
        #we then define our kernel remember that we have to go backwards through it so when compared to the
        #text book we go 4,3,2,1.  Each entry in this list is representative of a pixel
        kernel = [[y-1,x],[y,x-1],[y+1,x],[y,x+1]]

        #we go through the pixels in our kernel list
        for pixel in kernel:
           
            try:
            #if the pixel is part of the object/white we append it's coordinates to the queue
                if pixel[0] >= 0 and pixel[1] >= 0: 
                    test_biome = inputImage[pixel[0]][pixel[1],0]
                    #print(test_biome)
                    
                    if  test_biome == current_biome:
                        #print('success')
                        crown_count.append(float(inputImage[pixel[0]][pixel[1],1]))
                        burn_queue.append(pixel)
                        inputImage[pixel[0],pixel[1]] = 0
            except IndexError:
                print ('out of bounds')

    def ignite(currentPixel, inputImage,blob_list,score):

        [y,x] = currentPixel
        
        #we burn the input image
        crown_count.append(float(inputImage[y][x,1]))
        inputImage[y,x] = 0

        #we assign the output image according to the current blob value 
        output_img[y,x] = current_id

        
        #we then call the function to identify the pixels around the current pixel being burned
        identifyIgnition([y,x],inputImage)

        #append the FIRST pixel to a list keeping track of all pixels in the blob
        blob_list.append(currentPixel)
       
        
        #we go through the pixels added to the burn queue by the IdentifyIgnition function
        while len(burn_queue) > 0:
            #use pop to remove the last pixel in the deque and assing it to a variable
            
            pixel = burn_queue.pop()

            

            #burn the pixel in the image at the coordinates in the burn_queue
            inputImage[pixel[0],pixel[1]] = 0

            #assign the pixel in output (at the coordinates in the burn_queue) according to the current_id 
            output_img[pixel[0],pixel[1]] = current_id
            
            #append the pixel to a list keeping track of all pixels in the blob
            blob_list.append(pixel)

            #identify if any adjacent pixels are to be burned
            identifyIgnition(pixel,inputImage)

    final_score = 0

    for biomes in possible_biomes:
        current_biome = biomes
        for y in range(5):
            for x in range(5):
                #we create an empty list that is going to contain the pixels of a blob, this is reset with every new blob
                blob_coordinates = []
                crown_count = []
                #we then check if the current pixel is white using foollwing if-statement
                if np_arr[y,x][0] == biomes:
                    
                    #we call our ignite function
                    ignite([y,x],np_arr,blob_coordinates,crown_count)

            

                    #once the mian part of the grass fire has been run we update the current blob ID
                    current_id = current_id+1 
                    

                    temp = [blob_coordinates,len(blob_coordinates)]

                    tile_and_size.append(temp)
                    
                    print(crown_count)
                    final_score = final_score + len(blob_coordinates)*sum(crown_count)

                    print("size of blob: "+ str(len(blob_coordinates))+'  blob of type: '+biomes +' fianl score: '+ str(final_score))
                    
                



    
  
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    



if __name__ == "__main__":
    main()





# look into this: https://techvidvan.com/tutorials/detect-objects-of-similar-color-using-opencv-in-python/






