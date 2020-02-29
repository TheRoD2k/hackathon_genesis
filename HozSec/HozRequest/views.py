from django.shortcuts import render
from django.shortcuts import redirect
import datetime
from .models import *
from . import db_functions
#размещение реквеста

def place_problem(request):
    #если не зареган - пиздуй на регистрацию
    #если вернулся после отправки формы - лети на problem_gained
    context = {}
    context["empty"] = False
    #request.session['login'] = "test@phystech.edu"
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

#регистрация
def signup(request):
    context = {}
    context['Match_passwords'] = False
    context['Empty_password'] = True
    context['initial'] = True #впервые грузится форма
    if(request.method == "POST"):
        context['initial'] = False
        context['Empty_password'] = (request.POST['pass_1']=="") or (request.POST['pass_2'] == "")
        context['Match_passwords'] = request.POST['pass_1'] == request.POST['pass_2']
        if(context['Empty_password'] or not context['Match_passwords']):
            return render(request, "HozRequest/reg_page.html", context)
        else:
            temp = User(password=request.POST['pass_1'],
                        email=request.POST['mail'],
                        ruleset='user',
                        name=request.POST['login'])
            request.session['login']=request.POST['mail']
            temp.save()
            return redirect("/public_problems/")
    return render(request,"HozRequest/reg_page.html",context)
def signin(request):
    context = {}
    context['wmail'] = False
    context['wpass'] = False
    if(request.method == "POST"):
        result = db_functions.login(request.POST["mail"],request.POST["pass"])
        if(result=='Successful log in'):
            request.session['login']=request.POST['mail']
            return redirect('/mainpage')
        elif result=='Wrong password':
            context['wpass'] = True
        else:
            context['wmail'] = True
    return render(request, "HozRequest/login_page.html", context)
def public_problems(request):
    context = {}
    context['requests'] = db_functions.get_public_problems()
    if context['requests'].exists():
        context['valid'] = True

    return render(request,"HozRequest/main_page.html", context)

def problem_info(request,problem_id):
    context = {}
    context['Failed'] = True
    temp_problem = db_functions.get_problem_by_id(problem_id)
    if temp_problem.exists():
        context['Failed'] = False


    return render(request,"HozRequest/problem.html",context)