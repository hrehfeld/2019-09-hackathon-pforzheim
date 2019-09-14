import requests
import sys
import json
import time
import os

filenames = sys.argv[1:]

v1_url = 'https://aihackathoncomputervision.cognitiveservices.azure.com/vision/v1.0/recognizeText?printed=true'
v2_url = 'https://aihackathoncomputervision.cognitiveservices.azure.com/vision/v2.0/recognizeText?mode=Printed&language=de'

url = v2_url

for filename in filenames:
    out_filename = filename + '.2.json'
    if os.path.exists(out_filename):
        continue

    data = {}
    headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': 'dfcc1195e70a44d7a4adfde1f075844d'}

    header_key = {'Ocp-Apim-Subscription-Key': 'dfcc1195e70a44d7a4adfde1f075844d'}

    with open(filename, 'rb') as f:
        r = requests.post(url, headers=headers, data=f.read())
        r.raise_for_status()
        next_url = r.headers['Operation-Location']
        print(next_url)

        while True:
            time.sleep(5)
            r2 = requests.get(next_url, headers=header_key)
            r2j = r2.json()
            if r2j.get('status', None) != 'Running' and not 'error' in r2j:
                with open(out_filename, 'w') as f:
                    json.dump(r2.json(), f)
                break


