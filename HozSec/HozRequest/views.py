from django.shortcuts import render

def mainpage(request):
    return render(request, 'HozRequest/example.html', {})

# Create your views here.
