from django.shortcuts import render
from . import models, forms
def mainpage(request):
    return render(request, 'HozRequest/example.html', {})
def signup(request):
    context={'filled':False}
    if request.method == 'POST':
        context["first"]=request.POST['first']
        context["filled"]=True

    return render(request, 'HozRequest/signup1.html', context)
def signin(request):
    return render(request, 'HozRequest/signin.html', {})
# Create your views here.
