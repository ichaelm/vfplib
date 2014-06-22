'''
Created on Jun 21, 2014

@author: Michael
'''

import numpy
import cv2

MATCH_THRESHOLD = 0.99

def threshold_image(im, threshold):
    newim = im.copy()
    array = newim.load()
    for x in xrange(newim.size[0]):
        for y in xrange(newim.size[1]):
            if array[x, y] > threshold:
                array[x, y] = 255
            else:
                array[x, y] = 0
    return newim

def find_subimage(pil_image, pil_template, searchbox = ()):
    image = numpy.array(pil_image).copy()#[:,:,::-1].copy() #split
    template = numpy.array(pil_template).copy()#[:,:,::-1].copy() #split
    offset = (0,0)
    if len(searchbox) == 4:
        left = searchbox[0]
        upper = searchbox[1]
        right = searchbox[2]
        lower = searchbox[3]
        image = image[upper:lower, left:right]
        offset = (left, upper)
    
    matchmatrix = cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)
    unresult = numpy.where(matchmatrix > MATCH_THRESHOLD)
    result = zip(unresult[1], unresult[0])
    result = [(coord[0]+offset[0], coord[1]+offset[1]) for coord in result]
    return result