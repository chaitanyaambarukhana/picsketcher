from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RegisteredUsers, Token
import jwt
import datetime
import re
import bcrypt


class Index(APIView):
    def post(self, request):
        return Response({"Success": True})

# Create your views here.


class Register(APIView):
    regex = '^[A-Za-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    message = ''

    def checkEmail(self, email):
        if(re.search(self.regex, email)):
            return False
        else:
            return True

    def password_check(self, passwd):
        SpecialSym = ['$', '@', '#', '%','!']
        val = False
        if len(passwd) < 8:
            val = True
            self.message = 'length should be at least 8'
            return val

        if len(passwd) > 20:
            val = True
            self.message = 'length should be not be greater than 20'
            return val
        if not any(char.isdigit() for char in passwd):
            val = True
            self.message = 'Password should have at least one numeral'
            return val
        if not any(char.isupper() for char in passwd):
            val = True
            self.message = 'Password should have at least one uppercase letter'
            return val
        if not any(char.islower() for char in passwd):
            val = True
            self.message = 'Password should have at least one lowercase letter'
            return val
        if not any(char in SpecialSym for char in passwd):
            val = True
            self.message = 'Password should have at least one of the symbols $@#'
            return val
        if val:
            return val

    def post(self, request):
        field_names = sorted(
            [field.name for field in RegisteredUsers._meta.get_fields()])
        request_keys = sorted(request.data.keys())
        field_names.remove("id")

        if request_keys != field_names:
            return Response("Some fields are missing.", status=status.HTTP_400_BAD_REQUEST)
        email = request.data["email"]
        password = request.data["password"]
        firstname = request.data["firstname"]
        lastname = request.data["lastname"]
        if self.checkEmail(email):
            return Response({"success": False, "message": "Unable to register---Invalid Email Format"})
        if (re.search('[^a-zA-Z]', firstname)) and (re.search('[^a-zA-Z]', lastname)):
            return Response({"success": False, "message": "Unable to register---Name Fields should be alphabetical"})
        if self.password_check(password):
            return Response({"success": False, "message": "incorrect password format--"+self.message})

        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(
            password=password.encode("ascii"), salt=salt)
        try:
            user = RegisteredUsers.objects.create(
                email=email,
                password=hashed_password.decode("ascii"),
                firstname=firstname,
                lastname=lastname
            )
            user.save()
        except:
            return Response({"success": False, "message": "Please enter a unique email"})

        return Response({"success": True, "message": "user successfully registered"})


class Login(APIView):

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"].encode('ascii')

        try:
            user = RegisteredUsers.objects.get(email=email)
        except:
            return Response({"success": False, "message": "User with the given email does not exist"})

        if bcrypt.checkpw(password, user.password.encode("ascii")):
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            fields = [f.name for f in Token._meta.get_fields()]
            
            try:
                token_user = Token.objects.create(token=token)
                token_user.save()
            except:
                return Response({"success": False, "message": "token creation failed"})
            response = Response()

            response.data = {"success": True, "message": "Successfully logged in",
                             'jwt': token_user.token, "First Name": user.firstname, "Last Name": user.lastname,"token_id":token_user.id}

            return response
        else:
            return Response({"success": False, "message": "Incorrect Passowrd"})


class LogOut(APIView):
    def post(self, request):
        id = int(request.data["id"])
        refresh_token = Token.objects.get(id =id)
        print(type(id))
        if not refresh_token:
            return Response({"success": False, "message": "unauthentiated"})
        try:
            refresh_token.delete()

            return Response({"success": True, "message": status.HTTP_205_RESET_CONTENT})
        except Exception as e:
            return Response({"success": False, "message": status.HTTP_400_BAD_REQUEST})
