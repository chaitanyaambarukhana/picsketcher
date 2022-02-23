
from django.contrib import admin
from django.urls import path
from registration import views as registration
from django.urls import include
from imagefilter import views as imagefilter

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include('rest_framework.urls')),
    path("register/", registration.Register.as_view()),
    path("login/", registration.Login.as_view()),
    path("filter/", imagefilter.Filter.as_view())
]
