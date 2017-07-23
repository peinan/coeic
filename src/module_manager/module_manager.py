#!/usr/bin/env python
# coding: utf-8
#
# Filename:   module_manager.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23


import sys, os
import subprocess, json


class ModuleManager:
  def __init__(self, upload_img_fp, coeic_root_path):
    self.upload_img_fp   = upload_img_fp
    self.upload_img_dir  = upload_img_fp.rsplit('/', 2)[1]
    self.coeic_root_path = coeic_root_path


  def main(self):
    result_split    = self.split_into_frames()
    result_extract  = self.extract_balloons(result_split)
    result_ocr      = self.ocr_texts(result_extract)
    result_recog    = self.recog_emotion(result_ocr)
    # result_generate = self.generate_speech(result_recog)

    result = result_split

    self.output_result(result)


  def split_into_frames(self):
    result = self.run_shell_script('split_into_frames', self.upload_img_fp)
    self.check_result(result)

    return result


  def extract_balloons(self, in_json):
    result = self.run_shell_script('extract_balloons', in_json)
    self.check_result(result)

    return result


  def ocr_texts(self, in_json):
    result = self.run_shell_script('ocr_texts', in_json)
    self.check_result(result)

    return result


  def recog_emotion(self, in_json):
    result = self.run_shell_script('recog_emotion', in_json)
    self.check_result(result)

    return result


  def generate_speech(self, in_json):
    result = self.run_shell_script('generate_speech', in_json)
    self.check_result(result)

    return result


  def run_shell_script(self, method_name, arg):
    method_fp = os.path.join(self.coeic_root_path,\
                             'src',\
                             method_name,\
                             "{}.py".format(method_name))

    process = subprocess.run(['python', method_fp, arg],\
                             stdout=subprocess.PIPE,\
                             stderr=subprocess.PIPE)
    result = process.stdout.decode('utf-8')

    return result


  def check_result(self, result_json):
    result = json.loads(result_json)
    if result['job_result']['status'] != 'SUCCEEDED':
      print(result)
      sys.exit(-1)


  def output_result(self, result):
    print(result)


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
  coeic_root_path = os.path.abspath(__file__).rsplit('/', 3)[0]
  module_manager = ModuleManager(upload_img_fp, coeic_root_path)
  module_manager.main()


if __name__ == '__main__':
  sys.path.append(os.path.abspath(__file__).rsplit('/', 2))
  main()

