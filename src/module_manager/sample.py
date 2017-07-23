#!/usr/bin/env python
# coding: utf-8
#
# Filename:   sample.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23

import subprocess, json, sys, os

def sample():
  dirpath = os.path.split(os.path.abspath(__file__))[0]
  script_fp = os.path.join(dirpath, 'module_manager.py')
  upload_img_path = os.path.join(script_fp.rsplit('/', 3)[0],\
                                 'data/upload_img_01/original.png')
  # print(script_fp, upload_img_path)
  result = subprocess.check_output('python {} {}'.format(script_fp, upload_img_path), shell=True, universal_newlines=True)

  print(result)


if __name__ == '__main__':
  sample()
