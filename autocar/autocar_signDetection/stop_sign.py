import cv2
import numpy as np
import requests
import ast


def stop_sign_detection(img, gray):

    url = "http://0.0.0.0:8000/stop/"

    casName = "stop_sign"
    cascPath = "./cascades/{}.xml".format(casName)
    signCascade = cv2.CascadeClassifier(cascPath)

    sign = signCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    for (x, y, w, h) in sign:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        distance = int((235 - w) / 3.5)

        if distance <= 30 and distance > 4:
            # get
            req = requests.get(url)
            dict_req = req.content.decode("UTF-8")
            dict_req = ast.literal_eval(dict_req)

            if dict_req["status"] == "done":
                # post
                post_data = {"status": "wait"}
                requests.post(url, data=post_data)
                print("post: stop")

    return img

