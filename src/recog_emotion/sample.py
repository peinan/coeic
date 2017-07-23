#!/usr/bin/env python
# coding: utf-8
#
# Filename:   sample.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23


import subprocess, json, os


def sample():
  dirpath = os.path.split(os.path.abspath(__file__))[0]
  script_fp = os.path.join(dirpath, 'recog_emotion.py')
  dummy_json_fp = os.path.join(dirpath, 'dummy_ocred_texts.json')
  dummy_json = json.dumps(json.loads(open(dummy_json_fp).read()), ensure_ascii=False)
  result = subprocess.check_output("python {} '{}'"\
      .format(script_fp, dummy_json), shell=True, universal_newlines=True)

  print(result)


if __name__ == '__main__':
  sample()

