from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse
from django.views.decorators import gzip
import cv2
import sys
import time

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()

    def get_frame(self):
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

        ret, image = self.video.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


        #faces = faceCascade.detectMultiScale(gray)

        ret,jpeg = cv2.imencode('.jpg',image)


        return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def index(request):
    return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
