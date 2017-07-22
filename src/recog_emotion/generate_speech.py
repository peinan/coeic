# coding: utf-8

import base64
import os
import json
import requests

URL = "http://rospeex.nict.go.jp/nauth_json/jsServices/VoiceTraSS"

def generate_speech(ocr_texts):
    i = 0
    databodys, response, wav, texts = [], [], [], []

    for n in range(0,len(ocr_texts["splited_frames"])):
        #渡されたjsonから、セリフを抜き出して、textsに格納していく
        texts.append(ocr_texts["splited_frames"][n]["extracted_balloons"][0]["texts"]["text"])

    for text in texts:
        #rospeexに渡す用のデータ作成
        databody = {"method": "speak",
                    "params": ["1.1",
                            {"language": "ja", "text":text,
                                "voiceType": "F117", "audioType": "audio/x-wav"}]}

        response.append(requests.post(URL, data=json.dumps(databody)))

        tmp = json.loads(response[i].text)
        wav.append(base64.decodebytes(tmp["result"]["audio"].encode("utf-8")))

        i = i + 1

    #./voice/　のディレクトリ数をfilesに代入
    files = len(os.listdir("./voice"))
    #新ディレクトリの数字
    new_dir_num = str(files + 1)
    #新ディレクトリのパス
    new_dir = "./voice/" + new_dir_num
    #新ディレクトリ作成
    os.mkdir(new_dir)

    for n in range(0, len(wav)):
        #新ディレクトリの中に、渡されたセリフの数だけ、.wavファイルを作成
        with open(new_dir + "/" + str(n) + ".wav", "wb") as f:
            f.write(wav[n])



if __name__ == "__main__":
    #テストjson
    ocr_texts = {
        "upload_img_path": "IMG_PATH",
        "splited_frames": [
            {
                "frame_img": "frame_img_01",
                "extracted_balloons": [
                    {
                        "balloon_img": "balloon_img1",
                        "texts": {
                            "text": "あいあいあいいあいあいあいあいあいあいあいあ",
                            "position": {
                                "left_upper": ["x"," y"],
                                "right_bottom": ["x", "y"],
                            }
                        }
                    },
                ]
            },{
                "frame_img": "frame_img_01",
                "extracted_balloons": [
                    {
                        "balloon_img": "balloon_img1",
                        "texts": {
                            "text": "ういういういういういういうういういういうい",
                            "position": {
                                "left_upper": ["x", "y"],
                                "right_bottom": ["x", "y"],
                            }
                        }
                    },
                ]
            }
        ]
    }
    generate_speech(ocr_texts)