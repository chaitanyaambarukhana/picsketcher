from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import RegisteredUsers


# Create your views here.
class Register(APIView):
    def post(self, request):
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
            return Response("Please enter a unique username or password")

        return Response({"success":True,"message":"user successfully registered"})


class Login(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        
        try:
            user = RegisteredUsers.objects.get(email=email)
            if user.password == password:
                return Response({"success":True, "message":"Successfully logged in"})
        except:
            return Response("User with the given email does not exist")
        
               