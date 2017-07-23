# coding: utf-8

import base64
import os
import json
import requests

URL = "http://rospeex.nict.go.jp/nauth_json/jsServices/VoiceTraSS"

def generate_speech(ocr_texts):
    i = 0
    databodys, response, wavs, texts, array_all_balloons = [], [], [], [], []
    array_all_frames = []
    array_all_wavs = []

    #
    #./voice/　のディレクトリ数をfilesに代入
    files = len(os.listdir("./voice"))
    #新ディレクトリの数字
    new_dir_num = str(files + 1)
    #新ディレクトリのパス
    new_dir = "./voice/" + new_dir_num
    #新ディレクトリ作成
    os.mkdir(new_dir)

    #TODO: フレームとバルーンの関係を知る
    #合計フレーム数
    all_frames_number = len(ocr_texts["splited_frames"])
    #合計フレームの配列
    array_all_frames = list(range(0,all_frames_number))

    for frame in array_all_frames:
        s = len(ocr_texts["splited_frames"][frame]["extracted_balloons"])
        array_all_balloons.append(s)

    #[1−1, 1-2, 2-1, 2-2...]の配列の作成
    for n in range(0,len(ocr_texts["splited_frames"])):
        for k in range(0, array_all_balloons[n]):
            array_all_wavs.append(str(n+1) + "-" + str(k+1))

    for n in range(0,len(ocr_texts["splited_frames"])):
        for k in range(0, array_all_balloons[n]):
            texts.append(ocr_texts["splited_frames"][n]["extracted_balloons"][k]["texts"]["text"])

    #print(texts)
    #['フレーム１のバルーン１', 'フレーム１のバルーン２', 'フレーム２のバルーン1', 'フレーム２のバルーン1', 'フレーム3のバルーン1', 'フレーム3のバルーン2', 'フレーム3のバルーン2']

    for text in texts:
        #rospeexに渡す用のデータ作成
        databody = {"method": "speak",
                    "params": ["1.1",
                               {"language": "ja", "text":text,
                                "voiceType": "F117", "audioType": "audio/x-wav"}]}

        response.append(requests.post(URL, data=json.dumps(databody)))

        tmp = json.loads(response[i].text)
        wavs.append(base64.decodebytes(tmp["result"]["audio"].encode("utf-8")))

        i = i + 1




    #TODO: バルーンを、フレーム-バルーン.wavの形で保存する
    w = 0
    for array_all_wav in array_all_wavs:
        with open(new_dir+ "/"+ str(array_all_wav)+ ".wav", "wb" ) as f:
            f.write(wavs[w])
        w = w + 1


if __name__ == "__main__":
    #テストjson
    ocr_texts = {
        "upload_img_path": "IMG_PATH",
        "splited_frames": [
            {
                "frame_img": "1",
                "extracted_balloons": [
                    {
                        "balloon_img": "1",
                        "texts": {
                            "text": "フレーム１のバルーン１",
                        }
                    },
                    {
                        "balloon_img":"2",
                        "texts":{
                            "text":"フレーム１のバルーン２"
                        }
                    }
                ]
            },{
                "frame_img": "2",
                "extracted_balloons": [
                    {
                        "balloon_img": "1",
                        "texts": {
                            "text": "フレーム２のバルーン1",
                        }
                    },
                    {
                        "balloon_img": "2",
                        "texts": {
                            "text": "フレーム２のバルーン2",
                        }
                    }
                ]
            },{
                "frame_img": "3",
                "extracted_balloons": [
                    {
                        "balloon_img": "1",
                        "texts": {
                            "text": "フレーム3のバルーン1",
                        }
                    },
                    {
                        "balloon_img": "2",
                        "texts": {
                            "text": "フレーム3のバルーン2",
                        }
                    },
                    {
                        "balloon_img": "3",
                        "texts": {
                            "text": "フレーム3のバルーン3",
                        }
                    }
                ]
            }
        ]
    }
    generate_speech(ocr_texts)