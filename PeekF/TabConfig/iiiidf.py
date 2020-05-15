
import sys
import os
import json
import django
from tqdm import tqdm
sys.setrecursionlimit(100000)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PeekPeek.settings")
django.setup()
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from PeekF.models import *

from django.views.decorators.csrf import csrf_protect
import pandas as pd
from PeekF.TabConfig.tabMonitor import retFilterFunc
from django.core.paginator import Paginator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


path0 = "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/"
path1 = "foxmail_v7.2.txt"
path2 = "notepad++_v7.6.4.txt"
path3 = "notepad.exe.txt"
path4 = "ultraiso_v9.6.53237.txt"
path5 = "winrar_v3.93.txt"
path6 = "wps_v19.552.txt"
path7 = "wechat_all.txt"


def printCount():

    path2_ = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/"+path2.split(".")[0]+"anay_tem_str.pkl")
    path3_ = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/"+path3.split(".")[0]+"anay_tem_str.pkl")
    path4_ = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/"+path4.split(".")[0]+"anay_tem_str.pkl")
    path5_ = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/"+path5.split(".")[0]+"anay_tem_str.pkl")
    path6_ = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/"+path6.split(".")[0]+"anay_tem_str.pkl")
    path7_ = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/"+path7.split(".")[0]+"anay_tem_str.pkl")
    vectorizer = CountVectorizer(token_pattern="\\b\\w+.\\w+\\b")
    m = []
    m.append(path2_)
    m.append(path3_)
    m.append(path4_)
    m.append(path5_)
    m.append(path6_)
    m.append(path7_)

    X = vectorizer.fit_transform(m)

    word = vectorizer.get_feature_names()
    weight = X.toarray()
    mm = [{},{},{},{},{},{}]

    for i in range(6):
        print(i)
        for j in range(len(word)):
            # print(word[j], ':', weight[i][j], end=' ', sep='')
            # print("\n")
            mm[i][word[j]] =  weight[i][j]

    for i in range(6):
        print(i)
        t = 0
        keee = sorted(mm[i].items(),key =lambda item:-item[1])
        n = 10
        for j in keee:
            if(n == 0):
                break
            print(j[0]," ",j[1] )
            # print()
            n -= 1
            t+=j[1]
        print(t/462796)
    pd.to_pickle(mm,"/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/mm_weight.pkl")
def checkCount():
    mm = pd.read_pickle( "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/mm_weight.pkl")
    keee = []
    for i in range(6):
        print(i)
        keee.append(sorted(mm[i].items(), key=lambda item: -item[1]))
        n = 10
        # for j in keee[-1]:
        #     if (n == 0):
        #         break
        #     print(j[0] )
        #     # print()
        #     n -= 1

    for j in range(10):
        m = ""
        for i in range(3):
            m += keee[i][j][0]
            m += " "
        print(m)


if __name__ == '__main__':
    checkCount()