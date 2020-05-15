from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_protect
import pandas as pd
import sys
import json
from PeekF.TabConfig.tabMonitor import retFilterFunc
from django.core.paginator import Paginator

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
    threadn_name = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_allthread.pkl")

    allInfo = []

    return render(request, 'navbar/nav_monitor.html',{'retFilterFunc_':retFilterFunc_,'threadn_name':threadn_name})

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
        threadn_name = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_allthread.pkl")

        page = request.GET.get('page')  # how many items per page
        num = request.GET.get('rows')
        page=622
        # num = 100

        right_boundary = int(page) * int(num)
        print(page, num, int(num)*(int(page)-1),right_boundary)
        threadd = '0009'

        lenth = threadn_name[threadd]
        if right_boundary > lenth:
            right_boundary = lenth
        rows = []
        rows_temp = []
        allInfo = BigBigtext.objects.filter(threadn=threadd,id__range=[int(num)*(int(page)-1),right_boundary])

        info = allInfo[0]


        search = ''
        if(search!=''):
            allInfo_tmp= BigBigtext.objects.filter(threadn=threadd, nameshow= search,d__range=[int(num) * (int(page) - 1), right_boundary])

            for i in allInfo_tmp:
                info = BigBigtext.objects.filter(threadn=threadd, id=1)[0]
                while(1):
                    if(info.pid == 0):
                        break

        while(1):
            if(info.pid == 0):
                break
            else:
                temp = BigBigtext.objects.filter(threadn=threadd,
                                                 id=info.pid)[0]
                info = temp
                rows_temp.append({'threadn': info.threadn, 'nameshow': info.nameshow, 'inputval': info.inputval, 'retvar': info.retval,
             'inputtype': info.inputtype, 'rettype': info.rettype,
             'group': info.group, 'file': info.file, 'childnum': info.childnum, 'id': info.id, 'pid': info.pid})


        rows_temp.reverse()
        rows = rows_temp

        for info in allInfo:
            rows.append({'threadn':info.threadn,'nameshow':info.nameshow,'inputval':info.inputval,'retvar':info.retval,'inputtype':info.inputtype,'rettype':info.rettype,
                               'group':info.group,'file':info.file,'childnum':info.childnum,'id':info.id,'pid':info.pid})

        # allInfo = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_bigger1.pkl")
        # # m = [allInfo['rows']

        data = {"total": lenth, "rows": rows}

        # p = Paginator(allInfo, 100)
        # if p.num_pages <= 1:  # 如果文章不足一页
        #     article_list = allInfo  # 直接返回所有文章
        #     data = ''  # 不需要分页按钮

        return HttpResponse(json.dumps(data), content_type="application/json")
    # return json
def tab_Compare_deal(request):
    # retFilterFunc_ = retFilterFunc()
    if request.method == "GET":
        print(request.GET)
        # threadn_name = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_allthread.pkl")

        page = request.GET.get('page')  # how many items per page
        num = request.GET.get('rows')
        # page=622
        # num = 100

        right_boundary = int(page) * int(num)
        print(page, num, int(num)*(int(page)-1),right_boundary)
        threadd = '0009'

        lenth = 280000
        if right_boundary > lenth:
            right_boundary = lenth
        rows = []
        rows_temp = []
        infos = PalPals2.objects.filter()#217779
        allInfo = BigBigtext.objects.filter(threadn=threadd,id__range=[186332,186332+300])

        info = allInfo[0]


        search = ''
        if(search!=''):
            allInfo_tmp= BigBigtext.objects.filter(threadn=threadd, nameshow= search,d__range=[int(num) * (int(page) - 1), right_boundary])

            for i in allInfo_tmp:
                info = BigBigtext.objects.filter(threadn=threadd, id=1)[0]
                while(1):
                    if(info.pid == 0):
                        break

        while(1):
            if(info.pid == 0):
                break
            else:
                temp = BigBigtext.objects.filter(threadn=threadd,
                                                 id=info.pid)[0]
                info = temp
                rows_temp.append({'nameshow': info.nameshow, 'inputval': info.inputval, 'retvar': info.retval,
             'inputtype': info.inputtype, 'rettype': info.rettype,
            'nameshow2': info.nameshow, 'inputval2': info.inputval, 'retvar2': info.retval,
                                'palsnum':0, 'id': info.id, 'pid': info.pid})


        rows_temp.reverse()
        rows = rows_temp

        for info in allInfo:
            infos = PalPals2.objects.filter(id=info.id)

            if(infos.count() == 0):
                rows_temp.append({'nameshow': info.nameshow, 'inputval': info.inputval, 'retvar': info.retval,
                                  'inputtype': info.inputtype, 'rettype': info.rettype,
                                  'nameshow2': " ", 'inputvar2': " ", 'retval2': " ",
                                  'palsnum': '-', 'id': info.id, 'pid': info.pid,'state':0})
            else:
                rows_temp.append({'nameshow': info.nameshow, 'inputval': info.inputval, 'retvar': info.retval,
                                  'inputtype': info.inputtype, 'rettype': info.rettype,
                                  'nameshow2': infos[0].nameshow2, 'inputvar2': "("+infos[0].inputval2+")", 'retval2':"("+infos[0].retval2+")",
                                  'palsnum': infos[0].palsnum, 'id': info.id, 'pid': info.pid,'state':infos[0].state})
        # allInfo = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_bigger1.pkl")
        # # m = [allInfo['rows']

        data = {"total": 300, "rows": rows}

        # p = Paginator(allInfo, 100)
        # if p.num_pages <= 1:  # 如果文章不足一页
        #     article_list = allInfo  # 直接返回所有文章
        #     data = ''  # 不需要分页按钮

        return HttpResponse(json.dumps(data), content_type="application/json")
    # return json
def tryboot(request):

    return render(request, 'tryboot.html')


def showlinediagram2(request):
    return render(request, 'chart/index.html')