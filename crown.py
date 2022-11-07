import cv2
import numpy as np;
 
# Read image
im = cv2.imread("C:/Users/chris/Documents/GitHub/king_domino/King Domino dataset/Cropped and perspective corrected boards/7.jpg")
 
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

b = im[:,:,0]




ret,thresh1 = cv2.threshold(b,100,255,cv2.THRESH_BINARY)


lower_crown = np.array([30,])
upper_crown = np.array([40,])

cv2.imshow('orig',im)
cv2.imshow('b',b)

cv2.waitKey(0)

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector()
 
# Detect blobs.
keypoints = detector.detect(im)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)