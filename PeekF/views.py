from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def index(request):
    if request.POST:
        p=Person(name=request.POST['name'],age=request.POST['age'])
        p.save()
    return getdata(request)

def getdata(request):
    list=Person.objects.all()
    print(list)
    return render(request, 'index.html',{'list':list})

def showlinediagram(request):
    return render(request, 'chart/showlinediagram.html')

def showNavBar(request):
    return render(request, 'navbar/index.html')

def showNavConf(request):
    return render(request, 'navbar/nav_conf.html')
