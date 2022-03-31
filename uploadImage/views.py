# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ImageStorage
import cv2
import base64
import numpy as np
import json
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import matplotlib.pyplot as plt


class UploadImage(APIView):
    def encode_tf_image(self,tensor):
        squeezed_numpy= np.squeeze(tensor.numpy())
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        # encoded_image_bytes = base64.b64encode(squeezed_numpy).decode('utf-8')
        encoded_image_bytes = base64.b64encode(squeezed_numpy)
        # r = base64.decodebytes(encoded_image_bytes)
        # q = np.frombuffer(r, dtype=np.float32)
        # arr1= np.reshape(q,(1500,1000,3))
        return encoded_image_bytes

    def load_image(self,image_base64):
        try:
            data = json.dumps({'image': image_base64})
        except:
            return Response({"success":False,"message":"error in loading json"})
        try:
            image = base64.b64decode(json.loads(data)['image'])
        except:
            return Response({"success":False,"message":"error in loading base64"})
        try:
            img = tf.image.decode_image(image, channels=3)
        except:
            return Response({"success":False,"message":"error in decoding tf image"})
        try:
            img = tf.image.convert_image_dtype(img, tf.float32)
        except:
            return Response({"success":False,"message":"Error in converting to float32"})
        img = img[tf.newaxis, :]
        return img
    def decode_image(self,img_base_64):
        try:
            # CV2
            jpg_original = base64.b64decode(img_base_64)
            jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            image_buffer = cv2.imdecode(jpg_as_np, flags=1)
        except:
            return Response({"success":False,"message":"error in decoding the bytes image"})
        return image_buffer

    def render_image(self,image):
        try:
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img_blur = cv2.GaussianBlur(img_gray, (45,45), 0, 0)
            img_blend = cv2.divide(img_gray, img_blur, scale=256)
        except:
            return Response({"success":False,"message":"Error in image filtering"})
        return img_blend

    def post(self, request):
        #Gray Filter OpenCV
        bytes_text = request.data["image_bytes"] #load image bytes
        image_s= self.decode_image(bytes_text) #decoding to np array
        image_filtered = self.render_image(image_s) #applying filters
        image_bytes = cv2.imencode('.jpg', image_filtered)#encoding filtered image
        jpg_as_text = base64.b64encode(image_bytes[1]) #storing in bytes
        #VanGogh Styling_Filter
        try:
            model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
        except:
            return Response({{"success":False,"message":"Error in loading model for VanGogh Styling"}})
        try:
            input_tensor = self.load_image(bytes_text)
        except:
            return Response({"success":False,"message":"Error in loading bytes of input image for VanGogh Styling"})
        #load style data
        f = open('uploadImage/data_filters/data.json')
        data = json.load(f)
        # Closing file
        f.close()
        van_style_bytes = data['data']['van_bytes']

        try:
            van_bytes_style_tensor = self.load_image(van_style_bytes)
        except:
            return Response({"success":False,"message":"Error in loading bytes of style image for VanGogh Styling"})
        image_result_van = model(tf.constant(input_tensor), tf.constant(van_bytes_style_tensor ))[0]
        jpg_as_text_van = self.encode_tf_image(image_result_van)

        #Chen Ke filtering
        chen_style_bytes = data['data']['chen_bytes']

        try:
            chen_bytes_style_tensor = self.load_image(chen_style_bytes)
        except:
            return Response({"success":False,"message":"Error in loading bytes of style image for Chen Ke Styling"})
        image_result_chen = model(tf.constant(input_tensor), tf.constant(chen_bytes_style_tensor ))[0]
        jpg_as_text_chen = self.encode_tf_image(image_result_chen)

        return Response({"success":True,"image_bytes":{"gray":jpg_as_text,"VanGogh":jpg_as_text_van,"chenki":jpg_as_text_chen}})
