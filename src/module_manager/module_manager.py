#!/usr/bin/env python
# coding: utf-8
#
# Filename:   module_manager.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23


class ModuleManager:
  def __init__(self, upload_img_fp):
    self.upload_img_fp = upload_img_fp


  def main(self):
    result_split    = self.split_into_frames()
    result_extract  = self.extract_balloons(result_split)
    result_ocr      = self.ocr_texts(result_extract)
    result_recog    = self.recog_emotion(result_ocr)
    result_generate = self.generate_speech(result_recog)


  def split_into_frames(self):
    pass


  def extract_balloons(self, in_json):
    pass


  def orc_texts(self, in_json):
    pass


  def recog_emotion(self, in_json):
    pass


  def generate_speech(self, in_json):
    pass


  def output_result(self):
    pass


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
  upload_img_fp = sys.argv[1]
  module_manager = ModuleManager(upload_img_fp)
  module_manager.main()



if __name__ == '__main__':
  main()
