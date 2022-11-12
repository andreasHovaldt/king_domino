from collections import deque
import numpy as np 
import cv2
import time



string_test = np.array([['field','swamp','field','mine','swamp'],
 ['mine', 'swamp', 'field', 'field', 'forest'],
 ['mine', 'swamp', 'start' ,'field', 'field'],
 ['mine' ,'mine', 'plains', 'plains', 'field'],
 ['field', 'field', 'swamp', 'swamp', 'plains']])


#first blob value 
current_id = 1


#burn queue
burn_queue = deque([])

output_img = np.zeros((string_test.shape[0],string_test.shape[1]), np.uint8)

#first function is to identify which pixels the fire should spread to after lit
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
                if inputImage[pixel[0],pixel[1]] == current_biome:
                    burn_queue.append(pixel)
                    inputImage[pixel[0],pixel[1]] = 0
        except IndexError:
            print ('out of bounds')
    


#following function is used to set the pixel values to either 1 or 0 
def ignite(currentPixel, inputImage,blob_list):

    
    
    [y,x] = currentPixel
    
    #we burn the input image
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

    
    
    
def compactness(blob_coordinates):
    
    #following line converts the given list of blob coordinates into a numpy array
    #this is done so it's possible to use numpy functions with it
    npBlob = np.array(blob_coordinates)

    npBlob

    max_valueY = np.max(npBlob[:,0])
   

    min_valueY =  np.min(npBlob[:,0])
    

    max_valueX = np.max(npBlob[:,1])
   

    min_valueX =  np.min(npBlob[:,1])


    area_of_blob = len(npBlob)

    compact = area_of_blob/(((max_valueY-min_valueY)+1)*((max_valueX-min_valueX))+1)

    print('compactness is '+str(compact))

    # #print('min value in Y '+ str(min_valueY))
    # print('max_value in Y '+str(max_valueY))

    # # #print('min value in X '+ str(min_valueX))
    # print('min value in y'+str(min_valueY))

    # #print('min value in Y '+ str(min_valueY))
    # print('max_value in X '+str(max_valueX))

    # # #print('min value in X '+ str(min_valueX))
    # print('min value in X'+str(min_valueX))


#this is the main loop of the program going through every pixel of the image
tile_and_size = list()

biome_array = ['mine','field','swamp','forest','plains','ocean']





for biomes in biome_array:
    current_biome = biomes
    for y in range(5):
        for x in range(5):
            #we create an empty list that is going to contain the pixels of a blob, this is reset with every new blob
            blob_coordinates = []
            #we then check if the current pixel is white using foollwing if-statement
            if string_test[y,x] == biomes:


                #we call our ignite function
                ignite([y,x],string_test,blob_coordinates)

        

                #once the mian part of the grass fire has been run we update the current blob ID
                current_id = current_id+1 
                

                temp = [blob_coordinates,len(blob_coordinates)]

                tile_and_size.append(temp)
                
                print("size of blob: "+ str(len(blob_coordinates))+'  blob of type: '+biomes)
                time.sleep(2)
                
                

print(tile_and_size) 

scale_val = 100
scaled_subtracted_frame = cv2.resize(output_img, None, fx= scale_val, fy= scale_val, interpolation= cv2.INTER_LINEAR)

cv2.imshow("test",scaled_subtracted_frame*100)
cv2.waitKey(0)