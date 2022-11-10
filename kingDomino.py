import cv2
from CrownDetect import CrownDetect
     
    
##----------------End of function definitions---------------##
def main():

    img = cv2.imread("King Domino dataset/Cropped and perspective corrected boards/6.jpg")

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

