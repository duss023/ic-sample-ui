#
# Copyright 2022 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
from logging import getLogger, Formatter, StreamHandler, FileHandler
import base64
from flask import Flask, render_template, request, send_file

import os
import time
import json
import requests
from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input as pi_resnet50
from tensorflow.keras.applications.xception import preprocess_input as pi_xception
from tensorflow.keras.applications.imagenet_utils import decode_predictions

LOG_FILE = 'logs/inference.log'

SERVICE_HOST = os.environ['IC_SAMPLE_API_SERVICE_HOST']
SERVICE_PORT = os.environ['IC_SAMPLE_API_SERVICE_PORT']

URL = 'http://' + SERVICE_HOST + ':' + SERVICE_PORT + '/v1/models/ic:predict'

logger = getLogger("Inference")
logger.setLevel(logging.DEBUG)
handler_format = Formatter('%(asctime)s [%(levelname)s] %(message)s')
stream_handler = StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(handler_format)
file_handler = FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

class Classifier:
    def __init__(self, model_type):
        self.model_type = model_type

    def classify(self, img):
        logger.info('classify start')
        if self.model_type == "xception":
            pil_img = Image.open(img).resize((299,299))
            preprocess = pi_xception
        else:
            pil_img = Image.open(img).resize((224,224))
            preprocess = pi_resnet50
        x = image.img_to_array(pil_img)
        x = np.expand_dims(x, axis=0)
        x = preprocess(x)

        payload = json.dumps(dict(instances=x.tolist()))

        st = time.time()
        r = requests.post(URL, data=payload)
        ed = time.time()
        logger.info('time(sec): {}'.format(ed - st))
            
        preds = np.asarray(json.loads(r.content.decode('utf-8'))['predictions'])
        res = decode_predictions(preds, top=5)
        cls = res[0][0][1]
        conf = res[0][0][2]
        logger.info('classify end (cls={} conf={})'.format(cls, str(conf)))
        return cls, conf

cfr=Classifier("resnet50")
#cfr=Classifier("xception")

app = Flask(__name__)

@app.route('/')
@app.route('/inference')
def inference():
    logger.info('inference')
    return render_template('inference.html', inf_img="", inf_class="", inf_conf="")

@app.route('/upload', methods=['POST'])
def upload():
    logger.info('upload')
    img = request.files['image']
    res_cls, res_conf = cfr.classify(img)
    img.seek(0)
    img_str = 'data:image/jpeg;base64,' + base64.b64encode(img.read()).decode('utf-8')
    return render_template('inference.html', inf_img=img_str, 
        inf_class=res_cls, inf_conf=str(res_conf))

@app.route('/log')
def log():
    with open(LOG_FILE, 'r') as f:
        log = f.readlines()
    return render_template('log.html', log_name=LOG_FILE, log_content=log)

@app.route('/download_log', methods=['POST'])
def download_log():
    logger.info('download_log')
    return send_file(LOG_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
