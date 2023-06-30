from django.db import models

# Create your models here.

class Image(models.Model):
    image_path = models.TextField(max_length=200)