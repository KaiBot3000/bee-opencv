# matplotlib doesn't like virtualenvs
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 

import os
import numpy as np
import cv2 as cv # opencv 3.4.0

# get images
dir_name = os.path.dirname(__file__)
single_color = cv.imread(os.path.join(dir_name, '../img/singleBee.png'))
comb_color = cv.imread(os.path.join(dir_name, '../img/combBee.png'))

# generate mask of matching template using contour of bee
single_gray = cv.cvtColor(single_color, cv.COLOR_BGR2GRAY)
# plt.imshow(single_bee_gray), plt.show() # for some reason flipping color channels, turning rainbow
# cv.imshow('bee', single_bee_gray)
# cv.waitKey(3000) # wait for 1s before continuing program
# cv.destroyAllWindows() # destroy, although this seems to happen anyhow

# flip channels- countouring works on black background, not white
single_flip = cv.bitwise_not(single_gray)
# cv.imshow('bee', single_bee_flip)
# cv.waitKey(3000) # wait for 1s before continuing program
# cv.destroyAllWindows() # destroy, although this seems to happen anyhow

# second argument is the cutoff; adjusted for my actual image down from 127
ret, threshold = cv.threshold(single_flip, 60, 255, 0)
single_contour, contours, hierarchy = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cv.imshow('bee', single_contour)
cv.waitKey(3000) # wait for 1s before continuing program
cv.destroyAllWindows() # destroy, although this seems to happen anyhow

