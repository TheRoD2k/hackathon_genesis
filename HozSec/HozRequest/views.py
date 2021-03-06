from django.shortcuts import render
from django.shortcuts import redirect
import datetime
from .models import *
from . import db_functions
from django.core.files.storage import FileSystemStorage
#размещение реквеста

def place_problem(request):
    """
    если не зареган - пиздуй на регистрацию
    если вернулся после отправки формы - лети на problem_gained
    """
    context = dict()
    context["empty"] = False
    mail = request.session.get('login',"")
    user = db_functions.get_user(mail)
    print(user.exists())
    if not user.exists():
        context["empty"] = True
    if request.method == 'POST':
        #здесь создание заявы и редирект, если пост не пустой
        if request.POST["theme"]=="":
            return render(request, 'HozRequest/place_problem.html', context)
        anonim = False
        try:
            anonim = (request.POST["anon"] == "on")
        except:
            pass
        temp = Request(date = datetime.datetime.now(),
                       theme = request.POST["theme"],
                       problem_text=request.POST["problem_text"],
                       user = user.get(),
                       private= anonim,
                       resolved=False)
        if not (request.FILES.get('myfile',None) is None):
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            fs.path("")
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)
            temp.photo_url = uploaded_file_url
        temp.save()
        return redirect("/userpage")
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
            return redirect('/public_problems')
        elif result=='Wrong password':
            context['wpass'] = True
        else:
            context['wmail'] = True
    return render(request, "HozRequest/login_page.html", context)



def public_problems(request):
    context = {}
    context['Logged'] = db_functions.get_user(request.session.get('login',"123")).exists()
    if request.method == "POST":
        req_id = int(request.POST['moderate'].split('+')[1])
        solved = request.POST['moderate'].split('+')[0]=='solved'
        Request.objects.filter(pk=req_id).update(resolved=solved)

    context['requests'] = db_functions.get_public_problems()
    tmp = []
    for i in context['requests']:
        tmp.append(db_functions.get_user_by_id(int(i['user_id']))['name'])
    context['zip'] = zip(context['requests'],tmp)
    context['isadmin'] = False
    if db_functions.get_user(request.session.get('login',"123")).exists():
        context['isadmin'] = (db_functions.get_user(request.session.get('login', "123"))[0].ruleset != 'user')
    if context['requests'].exists():
        context['valid'] = True

    return render(request,"HozRequest/main_page.html", context)

def problem_info(request,problem_id):
    context = {}
    context['Failed'] = True
    temp_problem = db_functions.get_problem_by_id(problem_id)
    context['Logged'] = db_functions.get_user(request.session.get('login',"123")).exists()
    if temp_problem.exists():
        if request.method == 'POST':
            tempouser = db_functions.get_user(request.session['login'])
            if tempouser.exists():
                temp_message = Message(request=Request.objects.get(id=problem_id),
                                       user=User.objects.get(email=tempouser[0].email),
                                       message_text=request.POST['message_text']
                                       )
                temp_message.save()

        context['Failed'] = False
        context['data'] = temp_problem[0]
        context['messages'] = db_functions.get_comments(problem_id)
        context['users'] = {}
        tem_mas = []
        for i in context['messages']:
            tempouser = db_functions.get_user_by_id(i['user_id'])
            tem_mas.append({'name': tempouser['name'],'role':tempouser['ruleset']})
        context['zip'] = zip(context['messages'],tem_mas)
        print(context['users'])

    return render(request,"HozRequest/problem.html",context)
def userpage(request):
    context = {}
    Logged = db_functions.get_user(request.session.get('login',"123")).exists()
    if not Logged:
        redirect("/signup")
    else:
        tempouser = db_functions.get_user(request.session.get('login',"123"))[0]
        context['problems'] = db_functions.get_problems_by_user(tempouser.id)
        context['user'] = tempouser
    return render(request,"HozRequest/userpage.html",context)

def logout(request):
    request.session['login']=""
    return redirect("/public_problems")