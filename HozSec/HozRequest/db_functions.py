from . import models as db
from .models import User, Message, Request
from django.db import models


def login(email, password):
<<<<<<< HEAD
    """
    login function
    :param email: user email
    :param password: user password
    :return: state
    """
    if User.objects.filter(email__exact=email, password__exact=password) is not None:
=======
    if User.objects.filter(email__exact=email, password__exact=password).exists():
>>>>>>> experimental_2
        return 'Successful log in'
    elif User.objects.filter(email__exact=email).exists():
        return 'Wrong password'
    else:
        return 'Wrong user'


def get_user(email):
    """
    :param email: user email
    :return: user by email
    """
    return User.objects.filter(email__exact=email)


def get_problems_by_user(email):
    """
    get all problems made by given user
    :param email: user email
    :return: dict of problems
    """
    return Request.objects.filter(user__exact=email).values()


def get_problems_to_make():
    """
    get all avaliable problems to resolve
    :return:
    """
    return Request.objects.filter(resolved__exact=False).values()


def get_public_problems():
    """
    get all public problems
    :return:
    """
    return Request.objects.filter(private__exact=False).values()

def get_problem_by_id(id):
    return Request.objects.filter(pk__exact = id).values()

def get_user_by_id(id):
    return User.objects.filter(pk__exact = id).values()[0]
def add_problem(email, theme, problem, private_flag):
    """
    add problem as default
    """
    db.create_request(db.RequestWrapper(
        theme_field=theme,
        problem_text_field=problem,
        private_field=private_flag,
        User_lnk=get_user(email)
    ))


def get_problems(user_email, problems_count=0):
    """
    :return: comments' themes for current user
    """
    return Request.objects.filter(user__email__exact=user_email).values('id', 'theme')


def get_problems_by_id(id_request):
    return Request.objects.filter(
        user__message__request__exact=id_request
    ).values('problem_text')


def get_messages(id_request):
    return Request.objects.filter(
        user__message__request_id__exact=id_request
    ).values('message_text')

def get_comments(problem_id):
    tempous = get_problem_by_id(problem_id)
    if not tempous.exists():
        return tempous
    else:
        tempous = tempous[0]
        return Message.objects.filter(request__exact=tempous['id']).values()
