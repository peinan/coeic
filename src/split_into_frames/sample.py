#!/usr/bin/env python
# coding: utf-8
#
# Filename:   sample.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23


from split_into_frames import FrameSplitter


def sample():
  upload_img_fp = 'sample_data/upload_img_01/original.png'
  frame_splitter = FrameSplitter(upload_img_fp)
  frame_splitter.main()


if __name__ == '__main__':
  sample()

