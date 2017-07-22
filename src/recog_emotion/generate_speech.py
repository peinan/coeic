# coding: utf-8

import base64
import json
import requests

URL = "http://rospeex.nict.go.jp/nauth_json/jsServices/VoiceTraSS"

def generate_speech(messages):

    databodys = []
    for message in messages:
        databody = {"method": "speak",
                    "params": ["1.1",
                            {"language": "ja", "text":message,
                                "voiceType": "F117", "audioType": "audio/x-wav"}]}
        databodys.append(databody)

    response = requests.post(URL, data=json.dumps(databodys))
    tmp = json.loads(response.text)
    wav = base64.decodebytes(tmp["result"]["audio"].encode("utf-8"))


    for i in range(0, len(message)):
        with open(str(i) + ".wav", "wb") as f:
            f.write(wav)



if __name__ == "__main__":
    messages = ["あああああ", "いいいいいい", "うううううううう"]
    generate_speech(messages)