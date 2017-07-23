# coding: utf-8

import json
import sys

if __name__ == '__main__':
    data = {
        'job_result': {
            'job_name': '[Class_name: method_name]',
            'status': 'SUCCEEDED',
            # 'status': 'FAILED',
            'message': 'error message here'
        },
        'upload_img_path': sys.argv[1],
        'splited_frames': [
            {
                'frame_img': 'img-1.png',
                'extracted_balloons': [
                    {
                        'texts': {
                            'speech': 'speech-1-1.wav'
                        }
                    }
                ]
            },
            {
                'frame_img': 'img-2.png',
                'extracted_balloons': [
                    {
                        'texts': {
                            'speech': 'speech-2-1.wav'
                         }
                    }
                ]
            }
        ]
    }
    print(json.dumps(data, ensure_ascii=False))
    # raise ValueError('value error')