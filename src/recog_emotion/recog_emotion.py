#!/usr/bin/env python
# coding: utf-8
#
# Filename:   recog_emotion.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23


import sys, traceback, os, json
try:
  import numpy as np
except:
  print(json.dumps(
    {'job_result':
      {'job_name': '[EmotionRecognizer: load modules]',
        'status': 'FAILED',
        'message': traceback.format_exc()}
    }
  ))
  sys.exit(-1)



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
    magnitudes = []
    for frame in frames:
      for balloon in frame['extracted_balloons']:
        texts = balloon['texts']
        n_text = len(texts['text'])
        area = self.calc_area(texts['position'])
        magnitude = self.calc_magnitude(n_text, area)
        magnitudes.append(magnitude)
    magnitudes = self.softmax(np.array(magnitudes))

    for i in range(len(frames)):
      for j in range(len(frames[i]['extracted_balloons'])):
        # 本当は i と j 両方考えたほうがいいけど、balloon は実質今ないので、
        # i のみ考えることにする
        m = magnitudes[i]
        frames[i]['extracted_balloons'][j]['texts']['emotion'] = {'magnitude': m}

    recoged_emotion = self.ocred_texts
    recoged_emotion['splitted_frames'] = frames

    return recoged_emotion


  def calc_area(self, position):
    area = (position['right_bottom'][0] - position['left_upper'][0]) *\
           (position['right_bottom'][1] - position['left_upper'][1])

    return area


  def calc_magnitude(self, n_text, area):
    return float(area) / n_text


  def softmax(self, x):
      c = np.max(x)
      exp_x = np.exp(x-c)
      sum_exp_x = np.sum(exp_x)

      return exp_x / sum_exp_x


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
  in_json = sys.argv[1]
  coeic_root_path = os.path.abspath(__file__).rsplit('/', 3)[0]
  emotion_recognizer = EmotionRecognizer(in_json, coeic_root_path)
  emotion_recognizer.main()


if __name__ == '__main__':
  main()
