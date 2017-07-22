# coding: utf-8

import base64
import json
import requests

URL = "http://rospeex.nict.go.jp/nauth_json/jsServices/VoiceTraSS"

def generate_speech(messages):

    databodys, response, wav = [], [], []
    i = 0
    for message in messages:
        databody = {"method": "speak",
                    "params": ["1.1",
                            {"language": "ja", "text":message,
                                "voiceType": "F117", "audioType": "audio/x-wav"}]}

        response.append(requests.post(URL, data=json.dumps(databody)))

        tmp = json.loads(response[i].text)
        wav.append(base64.decodebytes(tmp["result"]["audio"].encode("utf-8")))

        i = i + 1


    for n in range(0, len(wav)):
        with open(str(n) + ".wav", "wb") as f:
            f.write(wav[n])



if __name__ == "__main__":
    messages = ["いつまでも to you　", "いいいいいい", "うううううううう"]
    generate_speech(messages)