
from django.contrib import admin
from django.urls import path
from registration import views as registration
from uploadImage import views as uploadimg
from django.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', registration.Index.as_view()),
    path("auth/", include('rest_framework.urls')),
    path("register/", registration.Register.as_view()),
    path("login/", registration.Login.as_view()),
    path("logout/", registration.LogOut.as_view()),
    path('getuser/',registration.GetUser.as_view()),
    path("upload/", uploadimg.UploadImage.as_view()),
    path("updateuser/",registration.UpdateUser.as_view()),
    path("updatepassword/",registration.UpdatePassword.as_view()),
    path("save/",uploadimg.SaveImage.as_view())
]
