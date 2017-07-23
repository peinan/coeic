#!/usr/bin/env python
# coding: utf-8
#
# Filename:   split_into_frames.py
# Author:     Peinan ZHANG
# Created at: 2017-07-22

import json
import sys, io, os, traceback

try:
  import cv2
  from PIL import Image
  import numpy as np
except:
  print(json.dumps(
    {'job_name': '[Load modules: load modules]',
      'status': 'FAILED',
      'message': traceback.format_exc()}
  ))
  sys.exit(-1)

class FrameSplitter:
  def __init__(self, upload_img_fp):
    self.upload_img_fp = upload_img_fp


  def main(self):
    try:
      frame_positions = self.detect_frames()
      cropped_result = self.crop_frames(frame_positions)

      self.output_result(cropped_result)
    except:
      self.output_error('extract all frames', traceback.format_exc())


  def detect_frames(self):
    try:
      gray_img, result_img = self.load_img_set()
    except:
      self.output_error('load image set', traceback.format_exc())
    # ===> DEBUG
    # print("[DEBUG] load image: {}".format(self.upload_img_fp))
    # plt.imshow(gray_img, cmap='Greys_r')
    # plt.show()
    # <===

    # thresholding
    try:
      ret, thresh = cv2.threshold(gray_img, 80, 255, cv2.THRESH_BINARY_INV)
    except:
      self.output_error('1st thresholding', traceback.format_exc())
    # contours
    try:
      _, contours, hierarchy = cv2.findContours(thresh,\
                                                cv2.RETR_TREE,\
                                                cv2.CHAIN_APPROX_SIMPLE)
    except:
      self.output_error('1st contours', traceback.format_exc())
    # ===> DEBUG
    # rrr = cv2.imread(self.upload_img_fp)
    # for cnt in contours:
    #   cv2.drawContours(rrr, [cnt], -1, 255, 3)
    # plt.imshow(rrr)
    # plt.show()
    # <===
    # convex hull
    try:
      for c in contours:
        hull = cv2.convexHull(c)
        cv2.drawContours(result_img, [hull], -1, 255, -1)
    except:
      self.output_error('convex hull', traceback.format_exc())

    # ===> DEBUG
    # plt.imshow(result_img)
    # plt.show()
    # <===
    # detect rectangles
    try:
      frames = self.detect_shapes(result_img)
    except:
      self.output_error('detect rectangles', traceback.format_exc())

    return frames


  def load_img_set(self):
    img = cv2.imread(self.upload_img_fp)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return (gray_img, img)


  def detect_shapes(self, img):
    img = np.asarray(Image.fromarray(np.uint8(img)).convert('L'))
    retval, thresh = cv2.threshold(img, 127, 255, 1)
    _, contours, hierarchy = cv2.findContours(thresh, 1, 2)

    frame_positions = []
    for c in contours:
      approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c, True), True)
      try:
        frame_position = np.array(approx).reshape(4, 2)
      except ValueError:
        pass
      frame_positions.append(frame_position)

    return frame_positions


  def crop_frames(self, frame_positions):
    cropped_results = []
    rev_pos = list(reversed(frame_positions))
    orig_img = Image.open(self.upload_img_fp)
    for i in range(len(frame_positions)):
      box = self.generate_box(rev_pos[i])
      cropped_img = orig_img.crop(box)

      frame_img_fp = "sample_data/upload_img_01/frames/{:02d}.png".format(i+1)
      self.write_img(cropped_img, frame_img_fp)
      cropped_results.append(frame_img_fp)

    return cropped_results


  def generate_box(self, frame_position):
    postion = [ (xy[0], xy[1]) for xy in frame_position ]
    x_sorted_position = sorted(postion, key=lambda x: x[0])
    left_upper  = min(x_sorted_position[:2], key=lambda x: x[1])
    right_lower = max(x_sorted_position[2:], key=lambda x: x[1])

    return (left_upper[0], left_upper[1], right_lower[0], right_lower[1])


  def write_img(self, cropped_img, out_fp):
    img_dir = os.path.split(out_fp)[0]
    if not os.path.isdir(img_dir):
      os.makedirs(img_dir)
    cropped_img.save(out_fp, 'PNG')


  def output_result(self, cropped_result):
    print(
      json.dumps({
        'upload_img_path': self.upload_img_fp,
        'splited_frames': cropped_result
      })
    )


  def output_error(self, method_name, message):
    # build error message
    error = {
      'job_name': "[{}: {}]".format(self.__class__.__name__, method_name),
      'status': 'FAILED',
      'message': message
    }
    # json serialize
    print(json.dumps(error, ensure_ascii=False))
    sys.exit(-1)


def sample():
  upload_img_fp = 'sample_data/upload_img_01/original.png'
  frame_splitter = FrameSplitter(upload_img_fp)
  frame_splitter.main()


if __name__ == '__main__':
  sample()

