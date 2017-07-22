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

class OcrTexts:
  def __init__(self, in_json: str):
    extracted_balloons = self.parse_input(in_json)
    self.main(extracted_balloons)

  def main(self, extracted_balloons: dict):
    pass

  def parse_input(self, in_json: str) -> dict:
    pass

