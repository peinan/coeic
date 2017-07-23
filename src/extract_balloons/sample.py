#!/usr/bin/env python
# coding: utf-8
#
# Filename:   sample.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23


import subprocess, json


def sample():
  in_json_fp = 'dummy_splitted_frames.json'
  in_json = open(in_json_fp).read()
  result = subprocess.check_output("python extract_balloons.py '{}'"\
      .format(in_json), shell=True, universal_newlines=True)

  print(result)


if __name__ == '__main__':
  sample()

