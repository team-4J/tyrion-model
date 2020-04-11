from flask import Flask, request, Response
from random import randint
import jsonpickle
import numpy as np
import cv2
import subprocess

app = Flask(__name__)
random_min = 1000000000
random_max = 9999999999

@app.route('/execute/tyrion', methods=['POST'])
def test():
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    img_name = 'platesimg/' + str(randint(random_min, random_max)) + '.jpg'
    cv2.imwrite(img_name, img);

    bashCommand = "alpr " + str(img_name)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if "No license plates found" in output.decode('utf-8'): 
        to_return = {'message': 'not found'}
    else:
        result = output.decode("utf-8").split("-")[1]

        plate_result = result.split(" ")[1].split("\t")[0]
        score_result = result.split(" ")[3].split("\n")[0]
        to_return = {
            'license_plate': str(plate_result),
            'score': str(score_result)
        }

    response_pickled = jsonpickle.encode(to_return)

    return Response(response=response_pickled, status=200, mimetype="application/json")

app.run(host="0.0.0.0", port=8089)