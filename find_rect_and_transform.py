#!/usr/bin/env python

import numpy as np
import cv2
import os
import re
from os.path import isfile, join
import sys


def extract_rect(im):
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    
    ret,thresh = cv2.threshold(imgray, 127, 255, 0)
    
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_appr_SIMPLE)

    # finding contour with max area
    largest = None
    for cnt in contours:
        if largest == None or cv2.contourArea(cnt) > cv2.contourArea(largest):
            largest = cnt

    peri = cv2.arcLength(largest, True)
    appr = cv2.apprPolyDP(largest, 0.02 * peri, True)

    #cv2.drawContours(im, appr, -1, (0,255,0), 3)
    points_list = [[i[0][0], i[0][1]] for i in appr] 

    left  = sorted(points_list, key = lambda p: p[0])[0:2]
    right = sorted(points_list, key = lambda p: p[0])[2:4]

    print("l " + str(left))
    print("r " + str(right))

    lu = sorted(left, key = lambda p: p[1])[0]
    ld = sorted(left, key = lambda p: p[1])[1]

    ru = sorted(right, key = lambda p: p[1])[0]
    rd = sorted(right, key = lambda p: p[1])[1]

    print("lu " + str(lu))
    print("ld " + str(ld))
    print("ru " + str(ru))
    print("rd " + str(rd))

    lu_ = [ (lu[0] + ld[0])/2, (lu[1] + ru[1])/2 ]
    ld_ = [ (lu[0] + ld[0])/2, (ld[1] + rd[1])/2 ]
    ru_ = [ (ru[0] + rd[0])/2, (lu[1] + ru[1])/2 ]
    rd_ = [ (ru[0] + rd[0])/2, (ld[1] + rd[1])/2 ]

    print("lu_ " + str(lu_))
    print("ld_ " + str(ld_))
    print("ru_ " + str(ru_))
    print("rd_ " + str(rd_))

    src_pts = np.float32(np.array([lu, ru, rd, ld]))
    dst_pts = np.float32(np.array([lu_, ru_, rd_, ld_]))

    h,w,b = im.shape
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    print("H" + str(H))

    imw =  cv2.warpPerspective(im, H, (w, h))
    
    return imw[lu_[1]:rd_[1], lu_[0]:rd_[0]] # cropping image


def lowpass_filter(im):
    """
    This is the function to apply lowpass filter to image.

    """

    # FIXME: currently does not work, makes some strange dark band in the upper part of image

    h,w,b = im.shape
    im_fft = np.fft.fft2(im)
    fshift = np.fft.fftshift(im_fft)
    # fshift = im_fft

    crow,ccol = h/2 , w/2
    rrad = 0.75*crow
    crad = 0.75*ccol
    fshift[ crow-rrad:crow+rrad , ccol-crad:ccol+crad ] = 0
    #fshift[ 0:1000 , 0:1000 ] = 0
    #print fshift
    f_ishift = np.fft.ifftshift(fshift)
    # f_ishift = fshift

    img_back = np.fft.ifft2(f_ishift)
    imlp = np.abs(img_back)

    return imlp


if __name__ == "__main__":
    if len(sys.argv) > 1:
        mypaths = sys.argv[1:-1]
        mypaths = [i for i in mypaths if isfile(join(".", i))]
        outpath = sys.argv[-1]
    else:
        mypaths = ["."]
        outpath = ["."]


    for file in mypaths:
        print("Computing file " + file)

        try:
            im = cv2.imread(file)
            im = extract_rect(im)
            # im = lowpass_filter(im)

            outfile = re.sub("^.*/", outpath, file)
            cv2.imwrite(outfile, im)
        except:
            print("...failed")
            
            
            
        
        
