import os
import numpy as np
import cv2 as cv # opencv 3.4.0

# matplotlib doesn't like virtualenvs
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 

# courtesy https://www.pyimagesearch.com/2015/02/16/faster-non-maximum-suppression-python/
def supressNonMaxima(boxes, overlapThreshold):
    # check for an empty list of boxes
    if len(boxes) == 0:
        return []

    # # check for integers
    # if np.boxes.dtype.kind == 'i':
    #     boxes = np.boxes.astype('float')

    # boxes we'll keep
    pick = []

    # unpack coordinates of boxes
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]

    # compute area and sort boxes
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last] # maybe [-1] instead?
        pick.append(i)

        # create a meta bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.maximum(x2[i], x2[idxs[:last]])
        yy1 = np.maximum(y2[i], y2[idxs[:last]])

        # get dimensions of metabox
        w = np.maximun(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # get overlap
        overlap = (w * h) / area[idxs[:last]]

        # delete boxes with too much overlap
        idxs = np.delete(idxs, np.concatenate(([last],
            np.where(overlap > overlapThreshold)[0])))

    # return bounding boxes, as ints not floats
    return boxes[pick].astype('int')


if __name__ == '__main__':
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

    # Height and width of template for drawing rectangles later
    h, w = single_color.shape[:-1]

    # flip channels- countouring works on black background, not white
    single_flip = cv.bitwise_not(single_gray)

    # generate mask of template
    # second argument is the cutoff; adjusted for my actual image down from 127
    ret, mask = cv.threshold(single_flip, 60, 255, 0)

    ### Match against template and find best match

    result = cv.matchTemplate(comb_gray, single_gray, cv.TM_SQDIFF, mask)
    # result = cv.matchTemplate(comb_gray, single_gray, cv.TM_CCORR_NORMED)

    ### Single best match
    # min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    # print 'min:', min_val, ' max:', max_val
    # top_left = min_loc

    # Draw rectangle using match + height and width of template
    # bottom_right = (top_left[0] + w, top_left[1] + h)
    # cv.rectangle(comb_color, top_left, bottom_right, 255, 2)

    ### Multiple matches
    MATCH_THRESHOLD = 80000000 # min: 79277216.0, max: 146592384.0
    NMS_THRESHOLD = 0.0
    matches = np.where(result <= MATCH_THRESHOLD)
    print 'matches:', len(matches[0])
    boxes_unduped = np.array([])
    # boxes_unduped = []
    # unzip matches into points and add to boxlist
    for match in zip(*matches[::-1]):
        print 'match:', match
        top_left = match
        bottom_right = (match[0] + w, match[1] + h)
        box = np.array([top_left[0], top_left[1], bottom_right[0], bottom_right[1]])
        print 'box to add:', box
        boxes_unduped = np.concatenate(boxes_unduped, box)

    # boxes = supressNonMaxima(boxes_unduped, NMS_THRESHOLD)
    boxes = boxes_unduped
    print boxes

    for box in boxes:
        print 'hi'
        print 'box:', box
        cv.rectangle(comb_color, (box[0], box[1]), (box[2], box[3]), 255, 2)

    ### Show results

    # add some headspace between plots
    plt.subplots_adjust(hspace=0.5)

    # row, column, order (weird)
    # plt.subplot(411), plt.imshow(single_gray,cmap='gray')
    # plt.title('Template'), plt.xticks([]), plt.yticks([])

    # plt.subplot(412), plt.imshow(mask,cmap='gray')
    # plt.title('Mask'), plt.xticks([]), plt.yticks([])

    # plt.subplot(413), plt.imshow(result,cmap='gray')
    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])

    # plt and cv store images in reverse color: rgb v. bgr, so convert:
    plt.subplot(111), plt.imshow(cv.cvtColor(comb_color, cv.COLOR_BGR2RGB))
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])

    plt.show()
