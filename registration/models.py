from django.db import models


class RegisteredUsers(models.Model):
    email = models.EmailField(unique=True, blank=False,
                              max_length=250, null=False)
    password = models.CharField(max_length=200, blank=False, null=False)
    firstname = models.CharField(
        null=False, blank=False, max_length=250)
    lastname = models.CharField(
        null=False, blank=False, max_length=250)

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "users_data"


class Token(models.Model):
    token = models.CharField(max_length=1000, blank=False, null=False)

    def __str__(self) -> str:
        return self.token

    class Meta:
        db_table = "token_data"
