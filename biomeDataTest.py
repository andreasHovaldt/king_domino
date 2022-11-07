import cv2
import numpy as np

def get_hue_mean(img):
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    return np.mean(hsv_img[:,:,0])



#current_tile = cv2.imread("King Domino dataset/sorted_biome_tiles/mine_biome/3.jpg")
#current_tile = cv2.imread("King Domino dataset/sorted_biome_tiles/plains_house_biome/3.jpg")
#current_tile = cv2.imread("King Domino dataset/sorted_biome_tiles/forest_biome/9.jpg")
current_tile = cv2.imread("King Domino dataset/sorted_biome_tiles/ocean_biome/4.jpg")
#current_tile = cv2.imread("King Domino dataset/sorted_biome_tiles/swamp_house_biome/0.jpg")
#current_tile = cv2.imread("King Domino dataset/sorted_biome_tiles/field_house_biome/1.jpg")

current_tile = cv2.cvtColor(current_tile, cv2.COLOR_BGR2HSV)
current_tile_copy = np.copy(current_tile)


### Yellow sampling ###
yellow_sample = cv2.imread("King Domino dataset/sorted_biome_tiles/field_biome/0.jpg")
yellow_sample = yellow_sample[40:60,40:60,:]
yellow_hue_mean = get_hue_mean(yellow_sample)
yellow_lower = yellow_hue_mean * 0.85
yellow_upper = yellow_hue_mean * 1.2
print(f"mean:{yellow_hue_mean}  lower:{yellow_lower}  upper:{yellow_upper}")


### Green sampling ###
green_sample = cv2.imread("King Domino dataset/sorted_biome_tiles/plains_biome/0.jpg")
green_sample = green_sample[50:70,50:70,:]
green_hue_mean = get_hue_mean(green_sample)
green_lower = green_hue_mean * 0.8
green_upper = green_hue_mean * 1.3
print(f"mean:{green_hue_mean}  lower:{green_lower}  upper:{green_upper}")


### Blue sampling ###
blue_sample = cv2.imread("King Domino dataset/sorted_biome_tiles/ocean_biome/6.jpg")
blue_sample = blue_sample[40:60,40:60,:]
blue_hue_mean = get_hue_mean(blue_sample)
blue_lower = blue_hue_mean * 0.85
blue_upper = blue_hue_mean * 1.3
print(f"mean:{blue_hue_mean}  lower:{blue_lower}  upper:{blue_upper}")


### Red sampling ###
red_sample = cv2.imread("King Domino dataset/sorted_biome_tiles/plains_house_biome/4.jpg")
red_sample = red_sample[45:65,40:60,:]
red_hue_mean = get_hue_mean(red_sample)
red_upper = red_hue_mean * 1.4
red_lower = 255 - red_upper

print(f"mean:{red_hue_mean}  lower:{red_lower}  upper:{red_upper}")


#cv2.imshow("sample", red_sample)
#cv2.waitKey()

'''
mask = cv2.inRange(current_tile, yellow_lower, yellow_upper)

inverted_mask = mask>0
current_tile_empty_copy = np.zeros_like(current_tile, np.uint8)
white = np.full_like(current_tile, 255, np.uint8)
current_tile_empty_copy[inverted_mask] = white[inverted_mask]


cv2.imshow("Yellow sample", current_tile_empty_copy)
cv2.waitKey()
cv2.destroyAllWindows()
'''








yellow_count = 0
green_count = 0
blue_count = 0
red_count = 0

for y in range(current_tile.shape[0]):
    for x in range(current_tile.shape[1]):
        if current_tile[y,x,0] >= yellow_lower and current_tile[y,x,0] <= yellow_upper:
            #current_tile_copy[y,x,0] = 255
            yellow_count += 1
        if current_tile[y,x,0] >= green_lower and current_tile[y,x,0] <= green_upper:
            #current_tile_copy[y,x,0] = 255
            green_count += 1
        if current_tile[y,x,0] >= blue_lower and current_tile[y,x,0] <= blue_upper:
            #current_tile_copy[y,x,0] = 255
            blue_count += 1
        if current_tile[y,x,0] >= red_lower or current_tile[y,x,0] <= red_upper:
            #current_tile_copy[y,x,0] = 255
            red_count += 1
        else:
            current_tile_copy[y,x,0] = 0

print(f"y:{yellow_count}  r:{red_count}  g:{green_count}  b:{blue_count}")

cv2.imshow("or", cv2.cvtColor(current_tile, cv2.COLOR_HSV2BGR))
cv2.imshow("original", current_tile[:,:,0])
cv2.imshow("yellow", current_tile_copy[:,:,0])

cv2.waitKey()
cv2.destroyAllWindows()

