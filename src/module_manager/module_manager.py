#!/usr/bin/env python
# coding: utf-8
#
# Filename:   module_manager.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23


import sys, os
import subprocess, json
import logging

class ModuleManager:
  PYTHON_PATH = os.path.join(os.getenv('HOME'), ".pyvenv/default/bin/python")

  def __init__(self, upload_img_fp, coeic_root_path):
    self.upload_img_fp   = upload_img_fp
    self.upload_img_dir  = upload_img_fp.rsplit('/', 2)[1]
    self.coeic_root_path = coeic_root_path
    logger.debug("upload_img_dir: " + self.upload_img_dir)


  def main(self):
    result_split    = self.split_into_frames()
    result_extract  = self.extract_balloons(result_split)
    result_ocr      = self.ocr_texts(result_extract)
    result_recog    = self.recog_emotion(result_ocr)
    result_generate = self.generate_speech(result_recog)

    result = result_generate

    self.output_result(result)


  def split_into_frames(self):
    logger.debug("split_into_frames")
    result = self.run_shell_script('split_into_frames', self.upload_img_fp)
    logger.debug("split_into_frames result:" + result)
    self.check_result('split_into_frames', result)

    return result


  def extract_balloons(self, in_json):
    logger.debug("extract_balloons")
    result = self.run_shell_script('extract_balloons', in_json)
    logger.debug("extract_balloons result:" + result)
    self.check_result('extract_balloons', result)

    return result


  def ocr_texts(self, in_json):
    logger.debug("ocr_texts")
    result = self.run_shell_script('ocr_texts', in_json)
    logger.debug("ocr_texts result:" + result)
    self.check_result('ocr_texts', result)

    return result


  def recog_emotion(self, in_json):
    logger.debug("recog_emotion")
    result = self.run_shell_script('recog_emotion', in_json)
    logger.debug("recog_emotion result:" + result)
    self.check_result('recog_emotion', result)

    return result


  def generate_speech(self, in_json):
    logger.debug("generate_speech")
    result = self.run_shell_script('generate_speech', in_json)
    logger.debug("generate_speech result:" + result)
    self.check_result('generate_speech', result)

    return result


  def run_shell_script(self, method_name, arg):
    method_fp = os.path.join(self.coeic_root_path,\
                             'src',\
                             method_name,\
                             "{}.py".format(method_name))

    process = subprocess.run([self.PYTHON_PATH, method_fp, arg],\
                             stdout=subprocess.PIPE,\
                             stderr=subprocess.PIPE)
    result = process.stdout.decode('utf-8')

    return result


  def check_result(self, method_name, result_json):
    try:
      result = json.loads(result_json)
    except:
      self.output_error('check result: {}'.format(method_name), result_json)
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


def main(coeic_root_path):
  upload_img_fp = sys.argv[1]
  module_manager = ModuleManager(upload_img_fp, coeic_root_path)
  module_manager.main()


if __name__ == '__main__':
  src_dir_path = os.path.abspath(__file__).rsplit('/', 2)
  sys.path.append(src_dir_path)

  coeic_root_path = os.path.abspath(__file__).rsplit('/', 3)[0]

  # set up logger
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.DEBUG)

  log_dir = os.path.join(coeic_root_path, 'log')
  log_fp  = os.path.join(log_dir, "module_manager.log")
  if not os.path.isdir(log_dir):
    os.makedirs(log_dir)

  log_handler = logging.FileHandler(filename=log_fp)
  log_handler.setLevel(logging.DEBUG)
  log_handler.setFormatter(
      logging.Formatter(
        "[%(asctime)s][%(levelname)s](%(filename)s:%(lineno)s) %(message)s"
      ))
  logger.addHandler(log_handler)

  logger.debug("coeic_root_path:" + coeic_root_path)

  main(coeic_root_path)

