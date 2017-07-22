#!/usr/bin/env python
# coding: utf-8
#
# Filename:   split_into_frames.py
# Author:     Peinan ZHANG
# Created at: 2017-07-22

import cv2
from PIL import Image
import numpy as np

class FrameSplitter:
  def __init__(self, upload_img_fp):
    self.upload_img_fp = upload_img_fp


  def main(self):
    frames = self.detect_frames()
    result = self.crop_frames()


  def detect_frames(self):
    gray_img = self.load_gray_img(self.upload_img_fp)
    result_img = gray_img

    # thresholding
    ret, thresh = cv2.threshold(gray_img, 80, 255, cv2.THRESH_BINARY_INV)
    # contours
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # convex hull
    for c in contours:
      hull = cv2.convexHull(c)
      cv2.drawContours(result_img, [hull], -1, 255, -1)

    # detect rectangles
    frames = self.detect_shapes(result_img)

    return frames


  def load_gray_img(self, img_fp):
    img = cv2.imread(img_fp)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return img


  def detect_shapes(self, img):
    img = np.asarray(Image.fromarray(np.uint8(img)).convert('L'))
    retval, thresh = cv2.threshold(img, 127, 255, 1)
    _, contours, hierarchy = cv2.findContours(thresh, 1, 2)

    frames = []
    for c in contours:
      approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c, True), True)
      frames.append(approx)

    return frames


  def crop_frames(self):
    pass
