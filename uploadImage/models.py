from django.db import models
from django_base64field.fields import Base64Field
# from registration.models import RegisteredUsers

# Create your models here.


class ImageStorage(models.Model):
    image = Base64Field(max_length=9999, blank=False, null=False)
    filter = models.TextField(max_length=100,blank=False)
    user_id = models.IntegerField(blank=False)
    
    def __str__(self) -> str:
        return self.image

    class Meta:
        db_table = "Ima_bytes_data"
