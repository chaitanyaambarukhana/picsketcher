from dataclasses import field
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import RegisteredUsers

import numpy as np
import cv2
import base64

# Create your views here.


class Register(APIView):
    def post(self, request):

        field_names = sorted(
            [field.name for field in RegisteredUsers._meta.get_fields()])
        request_keys = sorted(request.data.keys())
        field_names.remove("id")

        if request_keys != field_names:
            return Response("Some fields are missing.", status=status.HTTP_400_BAD_REQUEST)

        email = request.data["email"]
        password = request.data["password"]
        username = request.data["username"]

        try:
            user = RegisteredUsers.objects.create(
                email=email,
                password=password,
                username=username
            )
            user.save()
        except:
            return Response("Please enter a unique username or email", status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": True, "message": "user successfully registered"}, status=status.HTTP_200_OK)


class Login(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        try:
            user = RegisteredUsers.objects.get(email=email)
            if user.password == password:
                return Response({"success": True, "message": "Successfully logged in"}, status=status.HTTP_200_OK)
        except:
            return Response("User with the given email does not exist", status=status.HTTP_400_BAD_REQUEST)
