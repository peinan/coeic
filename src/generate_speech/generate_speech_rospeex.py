#!/usr/bin/env python
# coding: utf-8
#
# Filename:   generate_speech.py
# Author:     Peinan ZHANG
# Created at: 2017-07-23


import base64, os, json
import requests


class SpeechGenerator:
  def __init__(self):
    self.URL = "http://rospeex.nict.go.jp/nauth_json/jsServices/VoiceTraSS"
    self.wavs = self.texts = self.array_all_balloons = self.array_all_frames= self.array_all_wavs= []
    self.new_dir = ""

  def main(self, ocr_text):
    self.make_directory()
    self.related_display(ocr_text)
    self.make_rospeex_file()
    self.save_rospeex_file()


  def make_directory(self):
    #./voice/　のディレクトリ数をfilesに代入
    files = len(os.listdir("./voice"))
    #新ディレクトリの数字
    new_dir_num = str(files + 1)
    #新ディレクトリのパス
    self.new_dir = "./voice/" + new_dir_num
    #新ディレクトリ作成
    os.mkdir(self.new_dir)


  def related_display(self, ocr_text):
    #合計フレーム数
    self.all_frames_number = len(ocr_text["splited_frames"])
    #フレーム数の配列
    self.array_all_frames = [x for x in range(self.all_frames_number)]

    self.array_all_balloons = [len(ocr_text["splited_frames"][x]["extracted_balloons"]) for x in self.array_all_frames]


    self.array_all_wavs = ["{}-{}".format(n+1,k+1) for n in range(len(ocr_text["splited_frames"])) for k in range(self.array_all_balloons[n]) ]


    self.texts = [ocr_text["splited_frames"][n]["extracted_balloons"][k]["texts"]["text"] for n in range(len(ocr_text["splited_frames"])) for k in range(self.array_all_balloons[n])]


  def make_rospeex_file(self):
    i = 0
    response = []
    for text in self.texts:
      #rospeexに渡す用のデータ作成
      databody = {"method": "speak",
                  "params": ["1.1",
                             {"language": "ja", "text":text,
                              "voiceType": "F117", "audioType": "audio/x-wav"}]}

      response.append(requests.post(self.URL, data=json.dumps(databody)))

      responce_json = json.loads(response[i].text)

      self.wavs.append(base64.decodebytes(responce_json["result"]["audio"].encode("utf-8")))

      i += 1

  def save_rospeex_file(self):
    w = 0
    for array_all_wav in self.array_all_wavs:
      with open(self.new_dir+ "/"+ str(array_all_wav)+ ".wav", "wb" ) as f:
          f.write(self.wavs[w])
      w += 1



def main():
  in_json = sys.argv[1]
  coeic_root_path = os.path.abspath(__file__).rsplit('/', 3)[0]
  speech_generator = SpeechGenerator()
  speech_generator.main(ocr_text)

if __name__ == "__main__":
    main()
