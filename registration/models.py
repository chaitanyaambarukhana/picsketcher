from enum import unique
from pyexpat import model
from turtle import back
from django.db import models

# Create your models here.


class RegisteredUsers(models.Model):
    email = models.EmailField(unique=True, blank=False,
                              max_length=250, null=False)
    password = models.CharField(max_length=500, blank=False, null=False)
    username = models.CharField(
        unique=True, null=False, blank=False, max_length=250)

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "registered_users"
