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
        'splited_frames': []
    }
    print(json.dumps(data, ensure_ascii=False))
    # raise ValueError('value error')