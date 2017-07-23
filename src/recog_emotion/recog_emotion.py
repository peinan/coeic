#!/usr/bin/env python
# coding: utf-8
#
# Filename:   recog_emotion.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23


import sys, traceback, os, json


class EmotionRecognizer:
  def __init__(self, in_json, coeic_root_path):
    self.ocred_texts = self.parse_input(in_json)
    self.upload_img_dir = self.ocred_texts['upload_img_path']\
                            .rsplit('/', 2)[1]
    self.coeic_root_path = coeic_root_path


  def main(self):
    frames = self.ocred_texts['splitted_frames']
    result = self.recognize_emotion(frames)

    self.output_result(result)


  def recognize_emotion(self, frames):
    for i in range(len(frames)):
      for j in range(len(frames[i]['extracted_balloons'])):
        frames[i]['extracted_balloons'][j]['texts']['emotion'] = {}

    recoged_emotion = self.ocred_texts
    recoged_emotion['splitted_frames'] = frames

    return recoged_emotion


  def parse_input(self, in_json):
    try:
      ocred_texts = json.loads(in_json)
    except:
      self.output_error('parse input', traceback.format_exc())

    return ocred_texts


  def output_result(self, result):
    job_result = {
        'job_name': '[{}: {}]'.format(self.__class__.__name__,\
                                      os.path.split(__file__)[-1]),
        'status': 'SUCCEEDED',
        'message': ''
    }
    result['job_result'] = job_result
    try:
      print(json.dumps(result, ensure_ascii=False))
    except:
      self.output_error('output result', traceback.format_exc())


def main():
  in_json = sys.argv[1]
  coeic_root_path = os.path.abspath(__file__).rsplit('/', 3)[0]
  emotion_recognizer = EmotionRecognizer(in_json, coeic_root_path)
  emotion_recognizer.main()


if __name__ == '__main__':
  main()
