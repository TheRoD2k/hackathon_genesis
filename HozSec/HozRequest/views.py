from django.shortcuts import render
from django.shortcuts import redirect
import datetime
from . import models, forms
from .models import *
from . import db_functions
def mainpage(request):

    return render(request, 'HozRequest/signin.html', {})
def place_problem(request):
    #если не зареган - пиздуй на регистрацию
    #если вернулся после отправки формы - лети на problem_gained
    context = {}
    context["empty"] = False
    request.session['login'] = "test@phystech.edu"
    mail = request.session.get('login',"")
    user = db_functions.get_user(mail)
    print(user.exists())
    if not user.exists():
        context["empty"] = True
    if request.method == 'POST':
        #здесь создание заявы и редирект, если пост не пустой
        if(request.POST["theme"]==""):
            return render(request, 'HozRequest/place_problem.html', context)
        temp = Request(date = datetime.datetime.now(),
                       theme = request.POST["theme"],
                       problem_text=request.POST["problem_text"],
                       user = user[0],
                       private= (request.POST["anon"] == "on"),
                       resolved=False)
        temp.save()
        return redirect("/")#заглушка
        return redirect("problem_gained/")
    return render(request, 'HozRequest/place_problem.html', context)
def signin(request):
    return render(request, 'HozRequest/signin.html', {})

# Create your views here.
