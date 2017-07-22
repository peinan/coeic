#!/usr/bin/env python
# coding: utf-8
#
# Filename:   ocr_texts.py
# Author:     Peinan ZHANG
# Created at: 2017-07-22

"""
IN
===
extracted_balloons = {
  "upload_img_path": "IMG_PATH",
  "splited_frames": [
    {
      "frame_img": "frame_img_01",
      "extracted_balloons": [
        "balloon_img1",
        "balloon_img2",
        ...
      ]
    },
    ...
  ]
}

OUT
====
ocred_texts = {
  "upload_img_path": "IMG_PATH",
  "splited_frames": [
    {
      "frame_img": "frame_img_01",
      "extracted_balloons": [
        {
          "balloon_img": "balloon_img1",
          "texts": {
            "text": "serif",
            "position": {
              "left_upper": [x, y],
              "right_bottom": [x, y],
            }
          }
        },
        ...
      ]
    },
    ...
  ]
}
"""

import json
import requests, io, os

# google api
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials
from google.cloud import vision

# import cv2
# import matplotlib.pyplot as plt
# from PIL import Image, ImageDraw

# import numpy as np


class OcrTexts:
  def __init__(self, in_json_fp):
    self.extracted_balloons = self.parse_input(in_json_fp)
    self.main(extracted_balloons)


  def main(self):
    # certification
    self.certify_google_api()

    frames = self.extracted_balloons['splited_frames']
    result_frames = []
    for frame in frames:
      for balloon in frame['extracted_balloons']:
        ocr_result = self.ocr_image(balloon)
        result = self.parse_ocr_result(ocr_result)
        frame['texts'] = result
        result_frames.append(frame)

    ocred_texts = self.extracted_balloons
    ocred_texts['splited_frames'] = result_frames

    self.output_result(ocred_texts)


  def parse_input(self, in_json_fp):
    in_json = json.load(open(in_json_fp), 'r')

    return in_json


  def certify_google_api(self):
    self.credentials = GoogleCredentials.get_application_default()
    self.vision_client = vision.Client()


  def ocr_image(self, balloon):
    # Loads a image into memory
    with io.open(balloon, 'rb') as img_file:
      content = img_file.read()
      img = vision_client.image(content=content)
      texts = img.detect_text()

    return texts


  def parse_ocr_result(self, ocr_result):
    description = text.description
    left_upper, right_upper, right_bottom, left_bottom = text.bounds.vertices

    result = {
      'text': description,
      'position': {
        'left_upper': [left_upper.x_coordinate, left_upper.y_coordinate],
        'right_bottom': [right_bottom.x_coordinate, right_bottom.y_coordinate],
      }
    }

    return result


  def output_result(self, ocred_texts):
    json.dumps(ocred_texts, ensure_ascii=False)


if __name__ == '__main__':
  json_fp = ''
  ocr = OcrTexts('')
  ocr.main()
