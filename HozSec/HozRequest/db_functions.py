from . import models as db
from .models import User, Message, Request
# from django.db import models


def login(email, password):
    if User.objects.filter(email__exact=email, password__exact=password).exists():
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
    return Request.objects.filter(user__exact=get_user(email).values('id')[0]['id']).values()


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


def get_problem_by_id(problem_id):
    return Request.objects.filter(pk__exact=problem_id)


def get_user_by_id(user_id):
    return User.objects.filter(pk__exact=user_id).values()[0]


def add_problem(email, theme, problem, private_flag):
    """
    add problem as default
    """
    try:
        rqst = Request(
            theme=theme,
            problem_text=problem,
            private=private_flag,
            user=User.objects.filter(email__exact=email)[0]
        )
        rqst.save()
    except IndexError:
        return 'No such user'


def get_problems(user_email, problems_count=0):
    """
    :return: comments' themes for current user
    """
    return Request.objects.filter(user__email__exact=user_email).values('id', 'theme')


def get_problems_by_id(request_id):
    return Request.objects.filter(
        pk__exact=request_id
    ).values('problem_text')


# def get_messages(request_id):
#     return Request.objects.filter(
#         pk__exact=request_id
#     ).values('message_text')


def get_comments(problem_id):
    tmp = get_problem_by_id(problem_id)
    # print(tmp)
    if not tmp.exists():
        return
    else:
        tmp = tmp.values()[0]
        return Message.objects.filter(request_id__exact=tmp['id']).values()
