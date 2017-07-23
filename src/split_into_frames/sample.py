#!/usr/bin/env python
# coding: utf-8
#
# Filename:   sample.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23


import os
from split_into_frames import FrameSplitter


def sample():
  coeic_root_path = os.path.abspath(__file__).rsplit('/', 3)[0]
  upload_img_fp = os.path.join(coeic_root_path, 'data/upload_img_01/original.png')
  frame_splitter = FrameSplitter(upload_img_fp, coeic_root_path)
  frame_splitter.main()


if __name__ == '__main__':
  sample()

