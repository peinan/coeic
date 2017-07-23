#!/usr/bin/env python
# coding: utf-8
#
# Filename:   sample.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23

import subprocess, json, sys, os

def sample():
  script_fp = os.path.abspath(__file__)
  upload_img_path = os.path.join(script_fp.rsplit('/', 3)[0],\
                                 'data/upload_img_01/original.png')
  print(script_fp, upload_img_path)
  # subprocess.check_output('python {} {}'.format(script_fp, upload_img_path))


if __name__ == '__main__':
  sample()
