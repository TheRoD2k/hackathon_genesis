from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
#fs = FileSystemStorage(location='/photos')

def user_ruleset_validator(ruleset):
    if ruleset != "admin" and ruleset != "user" and ruleset != "moderator":
        raise ValidationError('Incorrect ruleset: ' + ruleset)


class User(models.Model):
    email = models.EmailField()
    password = models.TextField()
    ruleset = models.TextField(validators=[user_ruleset_validator])
    name = models.CharField(max_length=15, default="")


class Request(models.Model):
    date = models.DateTimeField(auto_now=True)
    theme = models.CharField(max_length=200)
    problem_text = models.TextField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default="user")
    private = models.BooleanField(default=True)
    resolved = models.BooleanField(default=False)
    photo_url = models.CharField(max_length=200)


class Message(models.Model):
    request = models.ForeignKey(Request, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now=True)
    message_text = models.TextField(max_length=500)


# Create your models here.
