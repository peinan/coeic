#!/usr/bin/env python
# coding: utf-8
#
# Filename:   extract_balloons.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23


import sys, traceback, os, json
try:
  from PIL import Image
except:
  print(json.dumps(
    {'job_result':
      {'job_name': '[OcrTexts: load modules]',
        'status': 'FAILED',
        'message': traceback.format_exc()}
    }
  ))
  sys.exit(-1)


class BalloonExtractor:
  def __init__(self, in_json, coeic_root_path):
    self.splitted_frames = self.parse_input(in_json)
    self.upload_img_dir = self.splitted_frames['upload_img_path']\
                            .rsplit('/', 2)[1]
    self.coeic_root_path = coeic_root_path


  def main(self):
    frame_img_fns = self.splitted_frames['splitted_frames']
    result = self.extract_balloons(frame_img_fns)

    self.output_result(result)


  def parse_input(self, in_json):
    try:
      splitted_frames = json.loads(in_json)
    except:
      self.output_error('parse input', traceback.format_exc())

    return splitted_frames


  def extract_balloons(self, frame_img_fns):
    # TODO: use dummy data for now
    splitted_frames = []
    for frame_img_fn in frame_img_fns:
      frame_img_fp = os.path.join(self.coeic_root_path,\
                                  'data',\
                                  self.upload_img_dir,\
                                  'frames',\
                                  frame_img_fn)
      balloon_img_fn = "{}-1.png".format(frame_img_fn.split('.')[0])
      balloon_img_fp = os.path.join(self.coeic_root_path,\
                                  'data',\
                                  self.upload_img_dir,\
                                  'balloons',\
                                  balloon_img_fn)

      balloon_imgs = [balloon_img_fn]
      self.write_img(Image.open(frame_img_fp), balloon_img_fp)
      splitted_frames.append({'frame_img': frame_img_fn,\
                              'extracted_balloons': balloon_imgs})

    result = {'upload_img_path': self.splitted_frames['upload_img_path'],
              'splitted_frames': splitted_frames}

    return result


  def write_img(self, img, out_fp):
    img_dir = os.path.split(out_fp)[0]
    if not os.path.isdir(img_dir):
      os.makedirs(img_dir)
    img.save(out_fp, 'PNG')


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
      "job_result": {
        "job_name": "[{}: {}]".format(self.__class__.__name__, method_name),
        "status": 'FAILED',
        "message": message
      }
    }
    # json serialize
    print(json.dumps(error, ensure_ascii=False))
    sys.exit(-1)


def main():
  in_json = sys.argv[1]
  coeic_root_path = os.path.abspath(__file__).rsplit('/', 3)[0]
  balloon_extractor = BalloonExtractor(in_json, coeic_root_path)
  balloon_extractor.main()


if __name__ == '__main__':
  main()
