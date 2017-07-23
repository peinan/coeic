#!/usr/bin/env python
# coding: utf-8
#
# Filename:   sample.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23


from ocr_texts import OcrTexts


def sample():
  json_fp = 'dummy_extracted_balloons.json'
  ocr = OcrTexts(json_fp)
  ocr.main()


if __name__ == '__main__':
  sample()
