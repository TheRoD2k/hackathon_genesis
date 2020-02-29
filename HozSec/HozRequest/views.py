from django.shortcuts import render
from . import models, forms
def mainpage(request):
    return render(request, 'HozRequest/example.html', {})
def signup(request):
    context={}

    form = forms.RequestForm()
    if request.method == 'POST':
        form = forms.RequestForm(request.POST)
    return render(request, 'HozRequest/signup.html', {'form':form})
def signin(request):
    return render(request, 'HozRequest/signin.html', {})
# Create your views here.
