#!/usr/bin/env python
# coding: utf-8
#
# Filename:   ocr_texts.py
# Author:     Peinan ZHANG
# Created at: 2017-07-22

import json
import sys, io, os, traceback

try:
  import requests

  # google api
  from googleapiclient.discovery import build
  from oauth2client.client import GoogleCredentials
  from google.cloud import vision
except:
  print(json.dumps(
    {'job_name': '[Load modules: load modules]',
      'status': 'FAILED',
      'message': traceback.format_exc()}
  ))
  sys.exit(-1)


class OcrTexts:
  CURRENT_DIR     = os.getcwd()
  FRAME_IMG_DIR   = 'frames'
  BALLOON_IMG_DIR = 'balloons'


  def __init__(self, in_json):
    self.extracted_balloons = self.parse_input(in_json)
    # print('[DEBUG] INPUT:', self.extracted_balloons)


  def main(self):
    # certification
    try:
      self.certify_google_api()
    except:
      self.output_error('google api certification', traceback.format_exc())

    try:
      img_root_dir = os.path.split(self.extracted_balloons['upload_img_path'])[0]
      frames = self.extracted_balloons['splitted_frames']
    except:
      self.output_error('load data', traceback.format_exc())

    frame_results = []
    try:
      for frame in frames:
        balloon_results = []
        for balloon in frame['extracted_balloons']:
          balloon_fp = os.path.join(self.CURRENT_DIR,\
                                    img_root_dir,\
                                    self.BALLOON_IMG_DIR,\
                                    balloon)
          ocr_result = self.ocr_image(balloon_fp)
          result = self.parse_ocr_result(ocr_result)

          balloon_result = {'balloon_img': balloon}
          balloon_result['texts'] = result
          balloon_results.append(balloon_result)

          # print('[DEBUG] frame {} ballon {}'.format(frame['frame_img'], balloon))
          # print('[DEBUG] result:', result)

        frame_results.append({'frame_img': frame['frame_img'],\
                              'extracted_balloons': balloon_results})
    except:
      self.output_error('ocr all images', traceback.format_exc())

    ocred_texts = self.extracted_balloons
    ocred_texts['splitted_frames'] = frame_results

    self.output_result(ocred_texts)


  def parse_input(self, in_json):
    try:
      extracted_balloons = json.loads(in_json)
    except:
      self.output_error('parse_input', traceback.format_exc())

    return extracted_balloons


  def certify_google_api(self):
    self.credentials = GoogleCredentials.get_application_default()
    self.vision_client = vision.Client()


  def ocr_image(self, balloon_fp):
    # Loads a image into memory
    try:
      with io.open(balloon_fp, 'rb') as img_file:
        content = img_file.read()
        img = self.vision_client.image(content=content)
        texts = img.detect_text()
    except:
      self.output_error('ocr image', traceback.format_exc())

    return texts


  def parse_ocr_result(self, ocr_result):
    try:
      text = ocr_result[0]
      description = text.description
      left_upper, right_upper, right_bottom, left_bottom = text.bounds.vertices
    except:
      self.output_error('parse result', traceback.format_exc())

    result = {
      'text': description,
      'position': {
        'left_upper': [left_upper.x_coordinate, left_upper.y_coordinate],
        'right_bottom': [right_bottom.x_coordinate, right_bottom.y_coordinate],
      }
    }

    return result


  def output_result(self, ocred_texts):
    # print('RESULT\n======')
    try:
      print(json.dumps(ocred_texts, ensure_ascii=False))
    except:
      self.output_error('output result', traceback.format_exc())


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


def main():
  sys.argv[1]
  ocr = OcrTexts(sys.argv[1])
  ocr.main()


if __name__ == '__main__':
  main()
