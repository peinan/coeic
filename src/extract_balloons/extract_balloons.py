#!/usr/bin/env python
# coding: utf-8
#
# Filename:   extract_balloons.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23


import sys, traceback, os, json


class BalloonExtractor:
  def __init__(self, in_json):
    self.splitted_frames = self.parse_input(in_json)


  def main(self):
    frame_img_fps = self.splitted_frames['splitted_frames']
    result = self.extract_balloons(frame_img_fps)

    self.output_result(result)


  def parse_input(self, in_json):
    try:
      splitted_frames = json.loads(in_json)
    except:
      self.output_error('parse input', traceback.format_exc())

    return splitted_frames


  def extract_balloons(self, frame_img_fps):
    # TODO: use dummy data for now
    splitted_frames = []
    for frame_img_fp in frame_img_fps:
      balloon_imgs = [frame_img_fp]
      splitted_frames.append({'frame_img': frame_img_fp,\
                              'extracted_balloons': balloon_imgs})

    result = {'upload_img_path': self.splitted_frames['upload_img_path'],
              'splitted_frames': splitted_frames}

    return result


  def output_result(self, result):
    try:
      print(json.dumps(result, ensure_ascii=False))
    except:
      self.output_error('output result', traceback.format_exc())


def main():
  in_json = sys.argv[1]
  balloon_extractor = BalloonExtractor(in_json)
  balloon_extractor.main()


if __name__ == '__main__':
  main()
