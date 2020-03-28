from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_protect
import pandas as pd
import sys
import json
from PeekF.TabConfig.tabMonitor import retFilterFunc

def tab_home(request):
    return render(request, 'navbar/index.html')

def tab_Conf(request):
    dllandallfuncs = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/DLlandInfo.pkl")
    # print(newdisc)

    # dllandallfuncs = {("d1","cc"):["f1","f2"],("z1","ccc"):["f1","f2"],("a1","cccc"):["f1","f2"]}


    return render(request, 'navbar/nav_conf.html',{'dllandallfuncs':dllandallfuncs})

def tab_Monitor(request):
    retFilterFunc_ = retFilterFunc()
    # allInfo = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_bigger1.pkl")[0:10]
    allInfo = []

    return render(request, 'navbar/nav_monitor.html',{'retFilterFunc_':retFilterFunc_,'allInfo':allInfo})

def tab_Vis(request):


    return render(request, 'navbar/nav_vis.html')

def tab_Vis2(request):


    return render(request, 'navbar/nav_vis_anay.html')

def tab_Compare(request):


    return render(request, 'navbar/nav_compare.html')













@csrf_protect
def test(request):
    if request.POST:
        p=Person(name=request.POST['name'],age=request.POST['age'])
        p.save()
    return getdata(request)

def getdata(request):
    # list=Person.objects.all()
    list = Groupinfo.objects.all()
    print(list)

    return render(request, 'index.html',{'list':list})

def showlinediagram(request):
    return render(request, 'chart/showlinediagram.html')


def tab_Monitor_deal(request):
    # retFilterFunc_ = retFilterFunc()
    if request.method == "GET":
        print(request.GET)
        limit = request.GET.get('limit')  # how many items per page
        offset = request.GET.get('offset')

        allInfo = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_bigbigText1.pkl")
        # m = allInfo['rows']
        # data = {"total": 5, "rows": allInfo}

        return HttpResponse(json.dumps(allInfo), content_type="application/json")
    # return json

def tryboot(request):

    return render(request, 'tryboot.html')


def showlinediagram2(request):
    return render(request, 'chart/index.html')