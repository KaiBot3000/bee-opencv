# matplotlib doesn't like virtualenvs
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 

import os
import numpy as np
import cv2 as cv # opencv 3.4.0

### Load images

dir_name = os.path.dirname(__file__)

# use the lineup - template cut from match image
# single_color = cv.imread(os.path.join(dir_name, '../img/beeLineupSingle.png'))
# comb_color = cv.imread(os.path.join(dir_name, '../img/beeLineup.png'))

# use a realistic example
single_color = cv.imread(os.path.join(dir_name, '../img/singleBee.png'))
comb_color = cv.imread(os.path.join(dir_name, '../img/combBee.png'))

# Convert to greyscale for matching
single_gray = cv.cvtColor(single_color, cv.COLOR_BGR2GRAY)
comb_gray = cv.cvtColor(comb_color, cv.COLOR_BGR2GRAY)

# flip channels- countouring works on black background, not white
single_flip = cv.bitwise_not(single_gray)

# generate mask of template
# second argument is the cutoff; adjusted for my actual image down from 127
ret, mask = cv.threshold(single_flip, 60, 255, 0)

### Match against template and find best match

result = cv.matchTemplate(comb_gray, single_gray, cv.TM_SQDIFF, mask)
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
top_left = min_loc

### Show results

# Draw rectangle using match + height and width of template
h, w = single_color.shape[:-1]
bottom_right = (top_left[0] + w, top_left[1] + h)
cv.rectangle(comb_color, top_left, bottom_right, 255, 2)

# add some headspace between plots
plt.subplots_adjust(hspace=0.5)

# row, column, order (weird)
plt.subplot(411), plt.imshow(single_gray,cmap='gray')
plt.title('Template'), plt.xticks([]), plt.yticks([])

plt.subplot(412), plt.imshow(mask,cmap='gray')
plt.title('Mask'), plt.xticks([]), plt.yticks([])

plt.subplot(413), plt.imshow(result,cmap='gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])

# plt and cv store images in reverse color: rgb v. bgr, so convert:
plt.subplot(414), plt.imshow(cv.cvtColor(comb_color, cv.COLOR_BGR2RGB))
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])

plt.show()
