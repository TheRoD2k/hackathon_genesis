from . import models as db
from .models import User, Message, Request
from django.db import models


def login(email, password):
    if User.objects.filter(email__exact=email, password__exact=password).exists():
        return 'Successful log in'
    elif User.objects.filter(email__exact=email).exists():
        return 'Wrong password'
    else:
        return 'Wrong user'


def get_user(email):
    return User.objects.filter(email__exact=email)


def get_problems_by_user(email):
    return Request.objects.filter(user__exact=email).values()


def get_problems_to_make():
    return Request.objects.filter(resolved__exact=False).values()


def get_public_problems():
    return Request.objects.filter(private__exact=False).values()

def get_problem_by_id(id):
    return Request.objects.filter(pk__exact = id).values()

def get_user_by_id(id):
    return User.objects.filter(pk__exact = id).values()[0]
def add_problem(email, theme, problem, private_flag):
    db.create_request(db.RequestWrapper(
        theme_field=theme,
        problem_text_field=problem,
        private_field=private_flag,
        User_lnk=get_user(email)
    ))


def get_comments(problem_id):
    tempous = get_problem_by_id(problem_id)
    if not tempous.exists():
        return tempous
    else:
        tempous = tempous[0]
        return Message.objects.filter(request__exact=tempous['id']).values()
