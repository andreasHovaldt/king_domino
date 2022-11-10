import cv2
from CrownDetect import CrownDetect


#following function is used to slice the board into pieces and store them in the slice list
def slicing(frame):

    sliceList = []

    #extract the sice of the image
    height,width,channel = frame.shape

    #we know there are 25 equally sized squares and that the board itself is square allowing us to
    #to calculate the sice of a single square as following
    slice_width = int(width/5)
    slice_height = int(height/5)

    #following for loop will iterate through the squares
    for y in range(5):
        #here we append an array to the list 
        sliceList.append([])
        for x in range(5):
            #we calculate the slice itself
            square = frame[slice_height * y:slice_height*(y+1),slice_width * x:slice_width*(x+1)]

            #We append the square to a place in the list
            sliceList[y].append(square)
    return sliceList
            

#following function will be used to blur the images to a point where they are a solid colour
# Currently not used but could be helpful
def solidColour(slices, kernelSize):

    blurList=[]
    for i in range(5):
        blurList.append([])
        for j in range(5):
           blurList[i].append(cv2.GaussianBlur(slices[i][j],(kernelSize,kernelSize),0))

    return blurList

        
    
##----------------End of function definitions---------------##
def main():

    img = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/6.jpg")
    tile = cv2.imread("sorted_biome_tiles/field/field_house_biome/7.jpg")

    # Loading in the templates correlating to a crown on each type of tile...
    swamp_template = cv2.imread('King Domino dataset/Testing/swamp.jpg')
    forest_template = cv2.imread('King Domino dataset/Testing/forestCrown.jpg')
    mine_template = cv2.imread('King Domino dataset/Testing/mineCrown.jpg')
    ocean_template = cv2.imread('King Domino dataset/Testing/oceanCrown.jpg')
    field_template = cv2.imread('King Domino dataset/Testing/fieldCrown.jpg')
    grass_template = cv2.imread('King Domino dataset/Testing/grassCrown.jpg')
    # ... then package the templates into a list
    templates = [swamp_template,forest_template,mine_template,ocean_template,field_template,grass_template]


    
    # Display full image
    cv2.imshow('fullimg', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Initiate class object 
    cd = CrownDetect(img)
    print(cd.boxes)
    
    
    # Run class function to detect crowns on image
    print(cd.findCrowns(templates,0.6)) # <---- This apparently changes 'img'?
    
    
    # Display the final image 
    cv2.imshow("final1",cd.image)
    cv2.imshow("final2",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    main()

