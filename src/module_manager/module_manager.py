#!/usr/bin/env python
# coding: utf-8
#
# Filename:   module_manager.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23


import sys
import subprocess


class ModuleManager:
  def __init__(self, upload_img_fp):
    self.upload_img_fp = upload_img_fp


  def main(self):
    result_split    = self.split_into_frames()
    result_extract  = self.extract_balloons(result_split)
    result_ocr      = self.ocr_texts(result_extract)
    result_recog    = self.recog_emotion(result_ocr)
    result_generate = self.generate_speech(result_recog)

    self.output_result(result_generate)


  def split_into_frames(self):
    script = self.build_script('split_into_frames', self.upload_img_fp)
    result = self.run_shell_script(script)

    return result


  def extract_balloons(self, in_json):
    script = self.build_script('extract_balloons', in_json)
    result = self.run_shell_script(script)

    return result


  def orc_texts(self, in_json):
    script = self.build_script('ocr_texts', in_json)
    result = self.run_shell_script(script)

    return result


  def recog_emotion(self, in_json):
    script = self.build_script('recog_emotion', in_json)
    result = self.run_shell_script(script)

    return result


  def generate_speech(self, in_json):
    script = self.build_script('generate_speech', in_json)
    result = self.run_shell_script(script)

    return result


  def build_script(self, method_name, arg):
    return "python {method_name}/{method_name}.py '{arg}'"\
        .format(method_name=method_name, arg=arg)


  def run_shell_script(self, script):
    return subprocess.check_output(script, shell=True, universal_newlines=True)


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
  module_manager = ModuleManager(upload_img_fp)
  module_manager.main()


if __name__ == '__main__':
  sys.path.append(os.path.abs(__file__)).rsplit('/', 2)
  main()
