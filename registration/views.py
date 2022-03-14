from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RegisteredUsers,Token
import jwt, datetime
import re   
class Index(APIView):
    def post(self,request):
        return Response({"Success":True})

# Create your views here.
class Register(APIView):
    regex = '^[A-Za-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    message=''
    def checkEmail(self,email): 
        if(re.search(self.regex,email)): 
            return False
        else:
            return True 
    def password_check(self,passwd):
        SpecialSym =['$', '@', '#', '%']
        val = False
        if len(passwd) < 8:
            val=True
            self.message='length should be at least 8'
            return val
            
        if len(passwd) > 20:
            val = True
            self.message='length should be not be greater than 20'
            return val
        if not any(char.isdigit() for char in passwd): 
            val = True
            self.message='Password should have at least one numeral'
            return val
        if not any(char.isupper() for char in passwd):
            val = True
            self.message  ='Password should have at least one uppercase letter'
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
            return Response({"success":False,"message":"Unable to register---Invalid Email Format"})
        if (re.search('[^a-zA-Z]', firstname)) and (re.search('[^a-zA-Z]', lastname)):
            return Response({"success":False,"message":"Unable to register---Name Fields should be alphabetical"})
        if self.password_check(password):
            return Response({"success":False,"message":"incorrect password format--"+self.message})

        try:
            user = RegisteredUsers.objects.create(
            email=email,
            password=password,
            firstname=firstname,
            lastname=lastname
        )
            user.save()
        except:
            return Response({"success":False,"message":"Please enter a unique email"})

        return Response({"success":True,"message":"user successfully registered","name":firstname+" "+lastname})


class Login(APIView):
       
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        try:
            user = RegisteredUsers.objects.get(email=email)
            if user.password == password:
                payload={
                    'id': user.id,
                    'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat':datetime.datetime.utcnow()

                }
                token = jwt.encode(payload,'secret',algorithm='HS256')
                try:
                    token_user=Token.objects.create(token=token)
                    token_user.save()
                except:
                    return Response("token failed")
                response=Response()
                
                response.data= {"success":True, "message":"Successfully logged in",'jwt':token}
                      
                return response
            else:
                return Response({"success":False, "message":"Incorrect Passowrd"})
        except:
            return Response({"success":False,"message":"User with the given email does not exist"})
class LogOut(APIView):
    def post(self,request):
        refresh_token = Token.objects.all()
        if not refresh_token:
            return Response({"success":False,"message":"unauthentiated"})
        try:
            refresh_token.delete()

            return Response({"success":True,"message":status.HTTP_205_RESET_CONTENT})
        except Exception as e:
            return Response({"success":False,"message":status.HTTP_400_BAD_REQUEST})
        
        