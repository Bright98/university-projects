import cv2
import numpy as np
import requests
import ast


def traffic_light_detection(img, gray):
    def color_detection(img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        red_lower = np.array([161, 155, 84], np.uint8)
        red_upper = np.array([179, 255, 255], np.uint8)
        red_mask = cv2.inRange(hsv, red_lower, red_upper)

        green_lower = np.array([40, 50, 50], np.uint8)
        green_upper = np.array([90, 255, 255], np.uint8)
        green_mask = cv2.inRange(hsv, green_lower, green_upper)

        kernal = np.ones((5, 5), "uint8")

        red_mask = cv2.dilate(red_mask, kernal)
        res_red = cv2.bitwise_and(img, img, mask=red_mask)

        green_mask = cv2.dilate(green_mask, kernal)
        res_green = cv2.bitwise_and(img, img, mask=green_mask)

        contours, hierarchy = cv2.findContours(
            red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 300:
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # get
                req = requests.get(url)
                dict_req = req.content.decode("UTF-8")
                dict_req = ast.literal_eval(dict_req)

                if dict_req["status"] == "done":
                    # post
                    post_data = {
                        "command": "stop",
                        "status": "wait",
                    }
                    requests.post(url, data=post_data)
                    print("post: traffic_light [STOP]")

        contours, hierarchy = cv2.findContours(
            green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 300:
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # get
                req = requests.get(url)
                dict_req = req.content.decode("UTF-8")
                dict_req = ast.literal_eval(dict_req)

                if dict_req["status"] == "done":
                    # post
                    post_data = {
                        "command": "go",
                        "status": "wait",
                    }
                    requests.post(url, data=post_data)
                    print("post: traffic_light [GO]")

    url = "http://0.0.0.0:8000/traffic_light/"

    casName = "TrafficLight"
    cascPath = "./cascades/{}.xml".format(casName)
    signCascade = cv2.CascadeClassifier(cascPath)

    sign = signCascade.detectMultiScale(
        gray, scaleFactor=1.06, minNeighbors=3, flags=cv2.CASCADE_SCALE_IMAGE,
    )

    for (x, y, w, h) in sign:

        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        distance = int((170 - w) * (20 / 35))

        r = max(w, h) / 2
        centerx = x + w / 2
        centery = y + h / 2
        nx = int(centerx - r)
        ny = int(centery - r)
        nr = int(r * 2)
        crop_img = img[ny : ny + nr, nx : nx + nr]

        if distance <= 40 and distance > 4:
            color_detection(crop_img)

    return img
