from django.db import models
from django.core.exceptions import ValidationError


class UserWrapper:
    def __init__(self, email_field, password_field, ruleset_field):
        self.email = email_field
        self.password = password_field
        self.ruleset = ruleset_field


class RequestWrapper:
    def __init__(self, theme_field, problem_text_field, User_lnk, private_field=True, resolved_field=False):
        self.theme = theme_field
        self.problem_text = problem_text_field
        self.User = User_lnk
        self.private = private_field
        self.resolved = resolved_field


class MessageWrapper:
    def __init__(self, Request_lnk, User_lnk, message_text_field):
        self.Request = Request_lnk
        self.User = User_lnk
        self.message_text = message_text_field


def user_ruleset_validator(ruleset):
    if ruleset != "admin" and ruleset != "user" and ruleset != "moderator":
        raise ValidationError('Incorrect ruleset: ' + ruleset)


class User(models.Model):
    email = models.EmailField()
    password = models.TextField()
    ruleset = models.TextField(validators=[user_ruleset_validator])


class Request(models.Model):
    date = models.DateTimeField(auto_now=True)
    theme = models.CharField(max_length=200)
    problem_text = models.TextField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    private = models.BooleanField(default=True)
    resolved = models.BooleanField(default=False)


class Message(models.Model):
    request = models.ForeignKey(Request, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now=True)
    message_text = models.TextField(max_length=500)


def create_user(UserWr):
    temp_user = User(email=UserWr.email,
                     password=UserWr.password,
                     ruleset=UserWr.ruleset)
    temp_user.save()
    return temp_user


def create_request(RequestWr):
    temp_request = Request(theme=RequestWr.theme,
                           problem_text=RequestWr.problem_text,
                           user=RequestWr.User,
                           private=RequestWr.private,
                           resolved=RequestWr.resolved)
    temp_request.save()


def create_message(MessageWr):
    temp_message = Message(request=MessageWr.Request,
                           user=MessageWr.User,
                           message_text=MessageWr.message_text)
    temp_message.save()


# temp_user_wrapper = UserWrapper(email_field="zhopa@phystech.edu", password_field="querty", ruleset_field="admin")
# temp_user = create_user(temp_user_wrapper)
#
# temp_request_wrapper = RequestWrapper(theme_field="Обосрали весь толчок...",
#                                       problem_text_field="Даже стульчак в говне...",
#                                       User_lnk=temp_user,
#                                       private_field=False)
# create_request(temp_request_wrapper)

# Create your models here.