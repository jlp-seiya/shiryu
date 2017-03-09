# Copyright 2016 Google Inc.
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

import logging
import json
import mydiff

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def hello():
    x = json.loads('{ "a":"b", "c": { "c":1} }')
    y = json.loads('{ "a":1, "b":[1,2]}')
    output = mydiff.diff(x,y)
    return "\n".join(output)


@app.route('/login', methods=['POST', 'GET'])
def login():
    aStr = request.form.get("aStr")
    bStr = request.form.get("bStr")
    logging.info("astr:%s" % aStr)
    logging.info("bstr:%s" % bStr)

    status = True
    try:
        x = json.loads(aStr)
    except:
        x = "Invalid Json"
        status = False
    try:
        y = json.loads(bStr)
    except:
        y = "Invalid Json"
        status = False

    if status:
        output = mydiff.diff_html(x, y)
        leftDiff = "<br/>".join(output[0])
        rightDiff = "<br/>".join(output[1])
    else:
        leftDiff = ""
        rightDiff = ""

    return render_template('template.html', 
        leftInput = x,
        rightInput = y,
        leftDiff = leftDiff,
        rightDiff = rightDiff)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
