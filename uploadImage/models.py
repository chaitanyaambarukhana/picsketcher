from django.db import models

# Create your models here.


class ImageStorage(models.Model):
    image = models.TextField(max_length=9999999999999999, blank=False, null=False)
    filter = models.TextField(max_length=100,blank=False)
    user_id = models.IntegerField(blank=False)
    date_created = models.DateTimeField()
    
    def __str__(self) -> str:
        return self.image

    class Meta:
        db_table = "Images_database"
