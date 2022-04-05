# Create your views here.

from tkinter import Image
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ImageStorage
import cv2
import base64
import numpy as np
import json
import tensorflow as tf
import tensorflow_hub as hub
import os
import matplotlib.pyplot as plt
import time
from django.http import JsonResponse




class UploadImage(APIView):
    def encode_tf_image(self,tensor):
        squeezed_numpy= np.squeeze(tensor.numpy())
        plt.imsave('data.png', squeezed_numpy)
        time.sleep(5)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        try:
            img_arr = cv2.imread('data.png')
        except:
            return Response({"success":False,"message":"error in imread of result image"})
        image_bytes = cv2.imencode('.png', img_arr)
        img_arr_orig = base64.b64encode(image_bytes[1])
        os.remove("data.png")
        return img_arr_orig

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
        bytes_type = request.data['style']
        #loading filters
        f = open('uploadImage/data_filters/data.json')
        data = json.load(f)
        f.close()
        
        try:
            model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
        except:
            return Response({{"success":False,"message":"Error in loading model for VanGogh Styling"}})
        try:
            input_tensor = self.load_image(bytes_text)
        except:
            return Response({"success":False,"message":"Error in loading bytes of input image for VanGogh Styling"})
        #load style data
        if bytes_type =='gray':
            image_s= self.decode_image(bytes_text) #decoding to np array
            image_filtered = self.render_image(image_s) #applying filters
            image_bytes = cv2.imencode('.jpg', image_filtered)#encoding filtered image
            image_bytes_b64 = base64.b64encode(image_bytes[1]) #storing in bytes

        elif bytes_type =='van':
            #VanGogh Styling_Filter
            van_style_bytes = data['data']['van_bytes']

            try:
                van_bytes_style_tensor = self.load_image(van_style_bytes)
            except:
                return Response({"success":False,"message":"Error in loading bytes of style image for VanGogh Styling"})
            image_result_van = model(tf.constant(input_tensor), tf.constant(van_bytes_style_tensor ))[0]
            image_bytes_b64 = self.encode_tf_image(image_result_van)
        elif bytes_type=='chen':
            #Chen Ke filtering
            chen_style_bytes = data['data']['chen_bytes']
            try:
                chen_bytes_style_tensor = self.load_image(chen_style_bytes)
            except:
                return Response({"success":False,"message":"Error in loading bytes of style image for Chen Ke Styling"})
            image_result_chen = model(tf.constant(input_tensor), tf.constant(chen_bytes_style_tensor ))[0]
            image_bytes_b64 = self.encode_tf_image(image_result_chen)
        #print(jpg_as_text_van)
        else:
            return Response({"success":False,"message":"Filter Not enrolled"})
        
        return Response({"success":True,"image_bytes":image_bytes_b64})

class SaveImage(APIView):
    def post(self,request):
        img_bytes = request.data['image_bytes']
        filter_type= request.data['filter_type']
        user_id= request.data['id']
        fields = [f.name for f in ImageStorage._meta.get_fields()]
        print(fields)
        
        try:
            img = ImageStorage.objects.create(image =img_bytes,filter=filter_type,user_id = user_id)
        except:
            return Response({"success":False,"message":"storing unsuccessful"})
        
        
        img.save()
        return Response({"success":True,"filter":img.filter,"user_id":img.user_id,"image_id":img.id})
    def get(self,request):
        id = request.data['id']
        try:
            data = ImageStorage.objects.filter(user_id=id).values()
        except:
            Response({"success":False,"message":"No data found"})
        return JsonResponse({"success":True,"image_data": list(data)})
    def delete(self, request):
        id = request.data['id']
        del_by_user= request.data['isUser']
        if del_by_user:
            del_item =ImageStorage.objects.filter(user_id=id)
        else:
            del_item = ImageStorage.objects.get(id=id)
        del_item.delete()
        return Response({"success":"True"})