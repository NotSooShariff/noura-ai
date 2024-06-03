import cv2
web_cam = cv2.VideoCapture(0)

def web_cam_capture():
    if not web_cam.isOpened():
        print("Error: Camera Failed")
        exit()

    path = 'webcam.jpg'
    ret, frame = web_cam.read()
    cv2.imwrite(path, frame)

web_cam_capture()