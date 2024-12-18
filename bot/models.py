from django.db import models

# Create your models here.

class TGUser(models.Model):
    user_id = models.BigIntegerField(primary_key=True, unique=True)


class Images(models.Model):
    image = models.FileField(upload_to='images/')
    user = models.ForeignKey(TGUser, on_delete=models.CASCADE)