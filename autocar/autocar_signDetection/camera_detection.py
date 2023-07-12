import urllib.request
import cv2
import numpy as np
import imutils
from traffic_light import traffic_light_detection
from stop_sign import stop_sign_detection

url = "http://YOURIP"
stream = urllib.request.urlopen(url)
bytes = b""

while True:
    bytes += stream.read(1024)
    a = bytes.find(b"\xff\xd8")
    b = bytes.find(b"\xff\xd9")
    if a != -1 and b != -1:
        jpg = bytes[a : b + 2]
        bytes = bytes[b + 2 :]
        jpg_buf = np.frombuffer(jpg, dtype=np.uint8)

        if len(jpg_buf) != 0:
            img = cv2.imdecode(jpg_buf, cv2.IMREAD_COLOR)
            img = imutils.resize(img, width=600)
            img = cv2.flip(img, 0)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            img = traffic_light_detection(img, gray)
            img = stop_sign_detection(img, gray)

            cv2.imshow("image", img)
            if cv2.waitKey(1) == 27:
                exit(0)

    else:
        pass
