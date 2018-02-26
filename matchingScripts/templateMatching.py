# matplotlib doesn't like virtualenvs
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 

import os
import numpy as np
import cv2 as cv # opencv 3.4.0

MATCH_THRESHOLD = 8

# get images
dir_name = os.path.dirname(__file__)
single_color = cv.imread(os.path.join(dir_name, '../img/singleBee.png'))
comb_color = cv.imread(os.path.join(dir_name, '../img/combBee.png'))

# generate mask of matching template using contour of bee
single_gray = cv.cvtColor(single_color, cv.COLOR_BGR2GRAY)
comb_gray = cv.cvtColor(comb_color, cv.COLOR_BGR2GRAY)

# flip channels- countouring works on black background, not white
single_flip = cv.bitwise_not(single_gray)

# generate mask of template
# second argument is the cutoff; adjusted for my actual image down from 127
ret, mask = cv.threshold(single_flip, 60, 255, 0)

# match template + mask + image 
matches = cv.matchTemplate(comb_gray, mask, cv.TM_SQDIFF)

match_location = np.where(matches < MATCH_THRESHOLD)
for point in zip(*match_location[::-1]):
    cv.rectangle(comb_color, point, (point[0], point[1]), (0,0,255), 2)
cv.imshow('bee', comb_color)
cv.waitKey(3000) # wait for 1s before continuing program
cv.destroyAllWindows() # destroy, although this seems to happen anyhow
