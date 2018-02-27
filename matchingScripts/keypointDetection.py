# matplotlib doesn't like virtualenvs
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 

import os
import numpy as np
import cv2 as cv # opencv 3.4.0

# read in images
dir_name = os.path.dirname(__file__)
single_bee_color = cv.imread(os.path.join(dir_name, '../img/singleBee.png'))
comb_bee_color = cv.imread(os.path.join(dir_name, '../img/singleCombBee.png'))

# convert to grayscale
single_bee_gray = cv.cvtColor(single_bee_color, cv.COLOR_BGR2GRAY)
comb_bee_gray = cv.cvtColor(comb_bee_color, cv.COLOR_BGR2GRAY)

# sift detector
orb = cv.ORB_create()

# find keypoints, descriptors using sift detector
keypoint_single, descriptor_single = orb.detectAndCompute(single_bee_gray, None)
keypoint_comb, descriptor_comb = orb.detectAndCompute(comb_bee_gray, None)

# orb match, then sort by distance
matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
matches = matcher.match(descriptor_single, descriptor_comb)
matches = sorted(matches, key = lambda x:x.distance)

# draw top ten
matches_drawn = cv.drawMatches(single_bee_gray, keypoint_single, comb_bee_gray, keypoint_comb, matches[:30], None, flags=2)
plt.imshow(matches_drawn), plt.show()
