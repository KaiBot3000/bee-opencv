# matplotlib doesn't like virtualenvs
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 

import numpy as np
import cv2 as cv # opencv 3.4.0

# read in images
single_bee_color = cv.imread('./img/singleCleanBee.png')
comb_bee_color = cv.imread('./img/combBee.png')

# convert to grayscale
single_bee_gray = cv.cvtColor(single_bee_color, cv.COLOR_BGR2GRAY)
comb_bee_gray = cv.cvtColor(comb_bee_color, cv.COLOR_BGR2GRAY)
# cv2.imshow('comb_bee_gray', comb_bee_gray)
# cv2.waitKey(1000) # wait for 1s before continuing program
# cv2.destroyAllWindows() # destroy, although this seems to happen anyhow

# sift detector
orb = cv.ORB_create()

# find keypoints, descriptors using sift detector
keypoint_single, descriptor_single = orb.detectAndCompute(single_bee_gray, None)
keypoint_comb, descriptor_comb = orb.detectAndCompute(comb_bee_gray, None)

kp_single_bee = cv.drawKeypoints(single_bee_gray, keypoint_single, None, color=(0,255,0), flags=0)
plt.imshow(kp_single_bee), plt.show()


# matcher = cv2.BFMatcher()