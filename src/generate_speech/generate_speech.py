#!/usr/bin/env python
# coding: utf-8
#
# Filename:   generate_speech.py
# Author:     Peinan ZHANG
# Created at: 2017-07-24


import os, sys, json, datetime, subprocess, time
import requests


class SpeechGenerator:
  API_KEY = '5949482e6f535537576b43437261794e436c5448765555723062687537476b7a6238676d6c325a49355441'
  URL = "https://api.apigw.smt.docomo.ne.jp/aiTalk/v1/textToSpeech?APIKEY=" + API_KEY

  TTS_CONFIG = {
      'speaker' : 'nozomi',
      'pitch' : '1',          # テキストを読み上げるベースライン・ピッチ（1.0: 0.5 - 2.0）
      'range' : '2',          # テキストを読み上げるピッチ・レンジ（1.0: 0.0 - 2.0）
      'rate' : '1',           # テキストを読み上げる速度（1.0: 0.5 - 4.0）
      'volume' : '0.5'        # テキストを読み上げる音量（1.0: 0.0 - 2.0）
  }

  def __init__(self, in_json, coeic_root_path):
    self.recoged_emotion = self.parse_input(in_json)
    self.upload_img_dir = self.recoged_emotion['upload_img_path']\
                            .rsplit('/', 2)[1]
    self.coeic_root_path = coeic_root_path
    self.cache_dir_fp = os.path.join(coeic_root_path,\
                                     'data',\
                                     self.upload_img_dir,\
                                     'cache')


  def main(self):
    frames = self.recoged_emotion['splitted_frames']
    result = self.generate_speeches(frames)

    self.output_result(result)


  def generate_speeches(self, frames):
    for i in range(len(frames)):
      for j in range(len(frames[i]['extracted_balloons'])):
        text = frames[i]['extracted_balloons'][j]['texts']['text']
        text = self.preprocess_text(text)
        config = self.generate_config(text)
        speech_fn = self.generate_speech(text,\
                                         config,\
                                         frames[i]['extracted_balloons'][j]['balloon_img'])
        frames[i]['extracted_balloons'][j]['texts']['speech'] = speech_fn
        time.sleep(1)

    result = self.recoged_emotion
    result['splitted_frames'] = frames

    return result


  def parse_input(self, in_json):
    try:
      recoged_emotion = json.loads(in_json)
    except:
      self.output_error('parse input', traceback.format_exc())

    return recoged_emotion


  def preprocess_text(self, text):
    text = text.replace('\n', ' ')

    return text


  def generate_config(self, text):
    # analyze text
    config = self.TTS_CONFIG
    if ("!" in text) or ("！" in text):
      config['volume'] = 2
      config['rate'] = 0.5

    return config


  def generate_speech(self, text, config, balloon_img):
    ssml = self.generate_ssml(text, config)
    response = self.get_api_response(ssml)
    cache_fn = balloon_img.rsplit('.')[0] + '.raw'
    cache_fp = os.path.join(self.cache_dir_fp, cache_fn)
    self.write_cache(response, cache_fp)
    speech_fn = self.convert_cache_wav(cache_fp)

    return speech_fn


  def generate_ssml(self, text, config):
    xml = """<?xml version="1.0" encoding="utf-8" ?><speak version="1.1"><voice name="{speaker}"><prosody rate="{rate}" pitch="{pitch}" range="{range}">{text}</prosody></voice></speak>""".format(**config, text=text)
    xml = xml.encode('utf-8')

    return xml


  def get_api_response(self, xml):
    response = requests.post(
      self.URL,
      data=xml,
      headers={
          'Content-Type': 'application/ssml+xml',
          'Accept' : 'audio/L16',
          'Content-Length' : str(len(xml))
      }
    )
    if response.status_code != 200 :
      self.output_error('get api response', "no response: {}".format(response.status_code))
    else:
      return response


  def write_cache(self, response, cache_fp):
    if not os.path.isdir(self.cache_dir_fp):
      os.makedirs(self.cache_dir_fp)

    with open(cache_fp, 'wb') as cache:
      cache.write(response.content)


  def convert_cache_wav(self, cache_fp):
    speech_fn = os.path.split(cache_fp)[-1].rsplit('.')[0] + '.wav'
    speech_dir = os.path.join(self.coeic_root_path,\
                            'data',\
                            self.upload_img_dir,\
                            'voice')
    if not os.path.isdir(speech_dir):
      os.makedirs(speech_dir)
    speech_fp = os.path.join(speech_dir, speech_fn)

    sox_cmd = "sox -t raw -r 16k -e signed -b 16 -B -c 1 {cache_fp} {speech_fp}"\
        .format(cache_fp=cache_fp, speech_fp=speech_fp)

    subprocess.check_output(sox_cmd, shell=True, universal_newlines=True)
    if os.path.isfile(speech_fp):
      return speech_fn
    else:
      self.output_error('convert_cache_wav', 'failed to convert')


  def output_result(self, result):
    job_result = {
        'job_name': '[{}: {}]'.format(self.__class__.__name__,\
                                      os.path.split(__file__)[-1]),
        'status': 'SUCCEEDED',
        'message': ''
    }
    result['job_result'] = job_result
    try:
      print(json.dumps(result, ensure_ascii=False))
    except:
      self.output_error('output result', traceback.format_exc())


  def output_error(self, method_name, message):
    # build error message
    error = {
      'job_result': {
        'job_name': "[{}: {}]".format(self.__class__.__name__, method_name),
        'status': 'FAILED',
        'message': message
      }
    }
    # json serialize
    print(json.dumps(error, ensure_ascii=False))
    sys.exit(-1)


def main():
  in_json = sys.argv[1]
  coeic_root_path = os.path.abspath(__file__).rsplit('/', 3)[0]
  speech_generator = SpeechGenerator(in_json, coeic_root_path)
  speech_generator.main()


if __name__ == '__main__':
  main()

