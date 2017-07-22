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
      "extracted_ballonns": [
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
ocr_texts = {
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
import matplotlib.pyplot as plt
# from PIL import Image, ImageDraw

# import numpy as np


class OcrTexts:
  def __init__(self, in_json_str):
    extracted_balloons = self.parse_input(in_json_str)
    self.main(extracted_balloons)


  def main(self, extracted_balloons):
    # certification
    self.certify_google_api()

    frames = extracted_balloons['splited_frames']
    for frame in frames:
      for balloon in frame['extracted_balloons']:
        ocr_result = self.ocr_image(balloon)
        result = self.parse_ocr_result(ocr_result)


  def parse_input(self, in_json_str):
    in_json = json(in_json_str)

    return in_json


  def certify_google_api(self):
    self.credentials = GoogleCredentials.get_application_default()
    self.vision_client = vision.Client()


  def ocr_image(self, balloon):
    # Loads a image into memory
    with io.open(balloon, 'rb') as img_file:
      content = img_file.read()
      img = vision_client.image(content=content)

    return img


  def parse_ocr_result(self, ocr_result):
    pass
