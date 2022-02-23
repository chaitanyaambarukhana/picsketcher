from django.shortcuts import render
import numpy as np
import cv2
import base64

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class Filter(APIView):
    def post(self, request):
        image = request.data["image"]
        image_np = np.fromstring(
            base64.b64decode(image.split(",")[1]), np.uint8)
        img_cv2 = cv2.imdecode(image_np, cv2.IMREAD_LOAD_GDAL)
        img_gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, ksize=(21, 21),
                                    sigmaX=1, sigmaY=1)

        filtered = cv2.divide(img_gray, 255-img_blur, scale=256)
        image_str = cv2.imencode("image_string.jpg", filtered)[1].tostring()
        img_encoded = base64.b64encode(image_str)
        return Response(img_encoded)
