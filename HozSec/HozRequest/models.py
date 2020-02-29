from django.db import models
class Request(models.Model):
    title = models.CharField(max_length=200)
    short_text = models.TextField()
    long_text = models.TextField()


# Create your models here.
