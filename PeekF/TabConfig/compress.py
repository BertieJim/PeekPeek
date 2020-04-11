

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


funcglobe = ['IsTextUnicode', 'InitCommonControlsEx', 'PrivateExtractIconsW', 'ImageList_CoCreateInstance',
             'CreateFontIndirectW', 'GetDeviceCaps', 'CreatePatternBrush', 'CreateSolidBrush', 'GetStockObject',
             'CreateRectRgn', 'CreateICA', 'CreateCompatibleDC', 'CreateDCA', 'CreateCompatibleBitmap', 'GetDIBits',
             'DeleteObject', 'TranslateCharsetInfo', 'CreatePalette', 'SelectPalette', 'GetObjectW', 'GetCurrentObject',
             'CreateDIBitmap', 'SelectObject', 'SetStretchBltMode', 'SetBkColor', 'SetTextColor', 'GetDIBColorTable',
             'StretchDIBits', 'CreateBitmap', 'BitBlt', 'DeleteDC', 'GetTextMetricsW', 'CreateRoundRectRgn',
             'GetViewportExtEx', 'GetWindowExtEx', 'GetLayout', 'GetGlyphIndicesW', 'GetTextAlign',
             'GetTextCharsetInfo', 'GetClipRgn', 'IntersectClipRect', 'GetMapMode', 'GetObjectType', 'GetObjectA',
             'GetOutlineTextMetricsW', 'GetFontData', 'GetTextFaceW', 'ExtSelectClipRgn', 'CreateDIBSection',
             'SetDIBits', 'SaveDC', 'GetClipBox', 'CreateRectRgnIndirect', 'ExtTextOutW', 'SetBkMode',
             'GetCurrentPositionEx', 'GetBkMode', 'SetTextAlign', 'MoveToEx', 'SelectClipRgn', 'CombineRgn', 'LPtoDP',
             'GetRandomRgn', 'GetRegionData', 'GetViewportOrgEx', 'SetICMMode', 'SetMapMode', 'SetViewportOrgEx',
             'SetWindowOrgEx', 'SetROP2', 'ModifyWorldTransform', 'GetDCOrgEx', 'StretchBlt', 'RestoreDC',
             'GetTextExtentPoint32W', 'TextOutW', 'GetBitmapBits', 'SetBitmapBits', 'CreateICW', 'EnumFontFamiliesExW',
             'GetOutlineTextMetricsA', 'Rectangle', 'SetDIBitsToDevice', 'GetTextCharacterExtra', 'CreateFontA',
             'RoundRect', 'ExcludeClipRect', 'PatBlt', 'GetPixel', 'GetEnhMetaFileW', 'GetBitmapDimensionEx',
             'RealizePalette', 'GdiplusStartup', 'GdipLoadImageFromStream', 'GdipCreateBitmapFromStream',
             'GdipGetImagePixelFormat', 'GdipGetImageHeight', 'GdipGetImageWidth', 'GdipBitmapLockBits',
             'GdipBitmapUnlockBits', 'GdipDisposeImage', 'GdipCreateBitmapFromScan0', 'GdipGetImageGraphicsContext',
             'GdipCreateSolidFill', 'GdipDrawImageRectI', 'GdipDeleteBrush', 'GdipDeleteGraphics', 'GdipCreateFromHDC',
             'GdipGetPropertyItemSize', 'GetForegroundWindow', 'GdipSetInterpolationMode', 'GdipCreatePen1',
             'GdipDrawRectangleI', 'GdipFillRectangleI', 'GdipCreateFontFromLogfontW', 'GdipDrawString',
             'GdipDeleteFont', 'GdipDrawLineI', 'GdipCreateBitmapFromHBITMAP', 'GdipGetImageEncodersSize',
             'GdipGetImageEncoders', 'GdipSaveImageToFile', 'GdipCreateBitmapFromFileICM', 'GdipDrawImageRectRectI',
             'ImmGetConversionStatus', 'ImmGetContext', 'ImmGetDefaultIMEWnd', 'ImmSetCompositionWindow',
             'ImmSetCompositionFontW', 'ImmReleaseContext', 'ImmNotifyIME', 'ImmEnumInputContext', 'GlobalAddAtomW',
             'FindAtomW', 'GetThreadPreferredUILanguages', 'GlobalFindAtomW', 'GlobalGetAtomNameW', 'GlobalDeleteAtom',
             'FindAtomA', 'GetTimeFormatW', 'GetACP', 'GetCPInfo', 'LCMapStringW', 'GetFileVersionInfoSizeW',
             'GetFileVersionInfoW', 'VerQueryValueW', 'CompareStringW', 'IsDBCSLeadByte', 'CharPrevA', 'CharNextA',
             'LCMapStringEx', 'GetThreadLocale', 'lstrcmpiA', 'CompareStringOrdinal', 'GetLocaleInfoEx',
             'GetSystemDefaultLCID', 'FindResourceW', 'LoadResource', 'SizeofResource', 'LockResource', 'lstrcmpA',
             'GetLocaleInfoW', 'CompareStringA', 'CharLowerA', 'lstrcmpW', 'CharPrevW', 'GetSystemDefaultUILanguage',
             'GetUserDefaultLCID', 'ConvertDefaultLocale', 'IsValidLocale', 'CharUpperW', 'GetUserDefaultLocaleName',
             'GetUserDefaultLangID', 'GetSystemDefaultLangID', 'CharLowerW', 'FreeResource', 'GetUserDefaultUILanguage',
             'GetThreadUILanguage', 'EnumResourceNamesExW', 'GetCPInfoExW', 'GetOEMCP', 'RegisterClassW',
             'CreateWindowExW', 'GetGUIThreadInfo', 'IsProcessDPIAware', 'GetDC', 'ReleaseDC', 'GetWindowDC',
             'IsWindow', 'GetPropW', 'DefWindowProcW', 'GetClassLongW', 'GetWindowLongW', 'SetPropW',
             'RegisterWindowMessageW', 'DestroyWindow', 'RemovePropW', 'UnregisterClassW', 'RegisterWindowMessageA',
             'SetWindowsHookExW', 'RegisterClassA', 'RegisterClipboardFormatW', 'RegisterClassExW',
             'EnumDisplayMonitors', 'GetMonitorInfoA', 'EnumDisplayDevicesA', 'SetTimer', 'CreateWindowExA',
             'ChangeWindowMessageFilter', 'DefWindowProcA', 'LoadIconW', 'LoadCursorW', 'GetClassInfoW',
             'SetWindowLongW', 'FindResourceExW', 'CallWindowProcW', 'DwmSetWindowAttribute', 'GetClientRect',
             'SetWindowPos', 'IsIconic', 'GetKeyboardLayout', 'ChangeWindowMessageFilterEx', 'LoadStringW',
             'SetWinEventHook', 'GetWindowThreadProcessId', 'GetFocus', 'SendMessageW', 'KillTimer',
             'PostThreadMessageW', 'RegisterTouchWindow', 'GetWindowRect', 'OffsetRect', 'SetWindowRgn', 'GetWindow',
             'InvalidateRect', 'MonitorFromWindow', 'GetMonitorInfoW', 'IsRectEmpty', 'IntersectRect', 'DrawTextW',
             'SetProcessDPIAware', 'GetWindowRgnBox', 'GetClassNameW', 'GetAncestor', 'MapWindowPoints', 'PostMessageW',
             'InternalGetWindowText', 'GetWindowTextW', 'GetWindowInfo', 'IsZoomed', 'SetRectEmpty', 'InflateRect',
             'SetRect', 'SendMessageTimeoutW', 'GetTitleBarInfo', 'EnumChildWindows', 'EnumDisplaySettingsW',
             'EnumDisplayDevicesW', 'GetQueueStatus', 'PeekMessageW', 'TranslateMessage', 'DispatchMessageW',
             'CallMsgFilterW', 'GetParent', 'LoadImageW', 'ShowWindow', 'SetForegroundWindow', 'IsHungAppWindow',
             'GetMessageW', 'ScreenToClient', 'GetCursorPos', 'PtInRect', 'GetKeyState', 'SetCursor', 'TrackMouseEvent',
             'GetUpdateRect', 'BeginPaint', 'EndPaint', 'EqualRect', 'UpdateLayeredWindow', 'GetIconInfo',
             'DestroyIcon', 'SetFocus', 'SetCapture', 'ReleaseCapture', 'GetClassNameA', 'GetShellWindow',
             'SendNotifyMessageW', 'MonitorFromRect', 'DrawIconEx', 'CopyImage', 'GetDoubleClickTime',
             'GetKeyboardLayoutList', 'RegisterClipboardFormatA', 'HideCaret', 'IsWindowVisible',
             'SetLayeredWindowAttributes', 'RegisterHotKey', 'FindWindowW', 'InSendMessageEx', 'IsTouchWindow',
             'UnregisterTouchWindow', 'wvsprintfW', 'GetMessageExtraInfo', 'ShowCaret', 'UpdateWindow', 'CreateCaret',
             'SetCaretPos', 'GetCaretPos', 'ClientToScreen', 'GetAsyncKeyState', 'ValidateRect', 'DestroyCaret',
             'GetDesktopWindow', 'FindWindowA', 'FindWindowExA', 'FillRect', 'GetDCEx', 'BringWindowToTop',
             'SwitchToThisWindow', 'WindowFromPoint', 'wsprintfW', 'OpenClipboard', 'EmptyClipboard',
             'SetClipboardData', 'CloseClipboard', 'PostMessageA', 'EnumThreadWindows', 'GetActiveWindow',
             'GetClipboardData', 'MonitorFromPoint', 'UnregisterHotKey', 'PostQuitMessage', 'UnhookWindowsHookEx',
             'UnregisterClassA', 'UnhookWinEvent', 'GetClassInfoExW']



path0 = "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/"
path1 = "foxmail_v7.2.txt"
path2 = "notepad++_v7.6.4.txt"
path3 = "notepad.exe.txt"
path4 = "ultraiso_v9.6.53237.txt"
path5 = "winrar_v3.93.txt"
path6 = "wps_v19.552.txt"
path7 = "wechat_all.txt"

def printCount():
    # threadn_name = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_allthread.pkl")
    # threadd = '0009'
    #
    # lenth = threadn_name[threadd]
    #
    alllist = []
    # 1744
    temp = []
    tem_str = ""
    # allinfo = BigBigtext.objects.filter(proid=proid)
    # for i in tqdm(allinfo):
    #     temp.append(i.dllname+'.'+i.apiname)
    #
    #
    #
    #     allinfo2 = BigBigtext.objects.filter(threadn=threadd,pid = i.id)
    #     for j in allinfo2:
    #         temp.append(j.nameshow)
    # tem_str = " ".join(temp)
    # tem_str = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/anay_tem_str.pkl")


    # print(tem_str)
    # input()
    # pattern = r''' (?x)         # set flag to allow verbose regexps
    # ([A-Z]\.)+          # abbreviations (e.g. U.S.A.)
    # | \w+(-\w+)*        # words with optional internal hyphens
    # | \$?\d+(\.\d+)?%?  # currency & percentages
    # | \.\.\.            # ellipses '''

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

    # m.append("user32IntersectRect user32IntersectRect")

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

    # pd.to_pickle(X,"/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/anay_X.pkl")


def getList(path):
    # f= open(path0+path)
    f = open("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/screenshot_trace_fixed_0009.txt")
    # try:
    lines = f.readlines()
    # except UnicodeDecodeError:

    temp = []
    for line in tqdm(lines):
        if "CALL" in line:

            dllname = ""
            funcname = ""
            try:
                dllname = line.split(' ')[1].split('_')[2].split(".")[0].strip()
                funcname = line.split(' ')[1].split('_')[2].split(".")[1].strip()
                inputvar = line.split(' ')[1].split('_')[3].strip()
                # thisone = (str(p2.findall(line)[0]).strip().split('.')[0].lower() )
                threadn = line.split(':')[0]

            except IndexError:
                print(line)
                print('iii1')
                pause = input()

            if funcname not in funcglobe:
                continue

            nameshow = str(dllname) + '.' + str(funcname)

            temp.append(nameshow)

    tem_str = " ".join(temp)
    pd.to_pickle(tem_str,"/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/"+path.split(".")[0]+"anay_tem_str.pkl")


def printtfIdf():
    pass

def getGroupSeriesSmall():
    # threadn_name = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_allthread.pkl")
    threadn_name = {'000d': 1075, '001b': 23, '001f': 13074, '0027': 593, '0026': 31, '000b': 23, '0009': 231380, '0036': 153, '002f': 4, '002d': 176, '003b': 3257, '003d': 3, '003e': 14, '003c': 3, '0051': 470, '0059': 454, '005b': 10, '005f': 8, '0067': 577, '006b': 3, '006d': 1, '006f': 4, '0074': 3, '0076': 2, '0079': 4, '0084': 32}
    print(threadn_name)
    threadd = '0009'
    # 2
    # 6
    # 22
    # 19
    # 0
    # 0
    # dict_keys(['Graphics and Gaming', 'Windows Application UI Development'])
    # 231380

    lenth = threadn_name[threadd]
    allinfo = BigBigtext.objects.filter(threadn=threadd)
    print(allinfo.count())
    # 1744
    temp = []
    y_axis = []
    x_axis = []
    biggroup = {}
    cc = {}

    cc1 = {}
    cc2 = {}
    cc3 = {}
    cc4 = {}
    cc5 = {}

    index = 1
    for i in tqdm(allinfo):
        # y_axis.append(i.group)
        temp = ''
        temp1 = ''
        temp2 = ''
        temp3 = ''
        temp4 = ''
        temp5 = ''
        try:
            temp = i.group.split('/')[0]
            temp1 = i.group.split('/')[0] + i.group.split('/')[1]
            temp2 = i.group.split('/')[0] + i.group.split('/')[1] + i.group.split('/')[2]
            temp3 = i.group.split('/')[0] + i.group.split('/')[1] + i.group.split('/')[2] + i.group.split('/')[3]
            temp4 = i.group.split('/')[0] + i.group.split('/')[1] + i.group.split('/')[2]+ i.group.split('/')[3]+ i.group.split('/')[4]
            temp5 = i.group.split('/')[0] + i.group.split('/')[1] + i.group.split('/')[2]+ i.group.split('/')[3]+ i.group.split('/')[4] + i.group.split('/')[5]
            print(temp)
            print(temp2)
            input()
        except IndexError:
            pass


        if(temp != '' and temp not in cc.keys()):
            cc[temp] = 0
        elif (temp != ''):
            cc[temp] += 1
        if (temp1 != '' and temp1 not in cc1.keys()):
            cc1[temp1] = 0
        elif (temp1 != ''):
            cc1[temp1] += 1
        if (temp2 != '' and temp2 not in cc2.keys()):
            cc2[temp2] = 0
        elif (temp2 != ''):
            cc2[temp2] += 1
        if (temp3 != '' and temp3 not in cc3.keys()):
            cc3[temp3] = 0
        elif (temp3 != ''):
            cc3[temp3] += 1
        if (temp4 != '' and temp4 not in cc4.keys()):
            cc4[temp4] = 0
        elif(temp4 != ''):
            cc4[temp4] += 1
        if (temp5 != '' and temp5 not in cc5.keys()):
            cc5[temp5] = 0
        elif (temp5 != ''):
            cc5[temp5] += 1
    # tem_str = " ".join(temp)

    print(len(cc))
    print(len(cc1))
    print(len(cc2))
    print(len(cc3))
    print(len(cc4))
    print(len(cc5))
    print(cc.keys())
    print(len(allinfo))


    pd.to_pickle(cc, "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/anay_cc.pkl")
    pd.to_pickle(cc1, "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/anay_cc1.pkl")
    pd.to_pickle(cc2, "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/anay_cc2.pkl")
    pd.to_pickle(cc3, "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/anay_cc3.pkl")
    pd.to_pickle(cc4, "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/anay_cc4.pkl")
    pd.to_pickle(cc5, "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/anay_cc5.pkl")

    # pd.to_pickle(y_axis, "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/anay_small_y_axis.pkl")
    # pd.to_pickle(biggroup, "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/anay_small_biggroup.pkl")


def getGroupSeriesSmallSmall():
    threadn_name = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_allthread.pkl")
    threadd = '0009'
    lenth = threadn_name[threadd]
    allinfo = BigBigtext.objects.filter(threadn=threadd, pid=0)
    # 1744
    temp = []
    y_axis = []
    x_axis = []
    biggroup = []
    index = 1
    for i in tqdm(allinfo):
        temp = i.group.split('/')[0]
        y_axis.append(temp)
        if (temp not in biggroup):
            biggroup.append(temp)
        # biggroup[temp].append(i.group)
        x_axis.append(index)
        index += 1

def howMany():
    result2 = ClangWineFunc.objects.filter()
    print(result2.count())

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


def printCount2():
    path2_ = pd.read_pickle(
        "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/" + path2.split(".")[0] + "anay_tem_str.pkl")
    path3_ = pd.read_pickle(
        "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/" + path3.split(".")[0] + "anay_tem_str.pkl")
    path4_ = pd.read_pickle(
        "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/" + path4.split(".")[0] + "anay_tem_str.pkl")
    path5_ = pd.read_pickle(
        "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/" + path5.split(".")[0] + "anay_tem_str.pkl")
    path6_ = pd.read_pickle(
        "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/" + path6.split(".")[0] + "anay_tem_str.pkl")
    path7_ = pd.read_pickle(
        "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/sel_soft_trace/" + path7.split(".")[0] + "anay_tem_str.pkl")

    vectorizer = CountVectorizer(token_pattern="\\b\\w+.\\w+\\b")
    m = []
    m.append(path2_)
    m.append(path3_)
    m.append(path4_)
    m.append(path5_)
    m.append(path6_)
    m.append(path7_)

    # m.append("user32IntersectRect user32IntersectRect")
    transformer = TfidfTransformer()
    X = vectorizer.fit_transform(m)
    tfidf = transformer.fit_transform(X)



    word = vectorizer.get_feature_names()
    weight = tfidf.toarray()
    mm = [{}, {}, {}, {}, {}, {}]
    nn = {}
    for i in range(6):
        print(i)
        for j in range(len(word)):
            # print(word[j], ':', weight[i][j], end=' ', sep='')
            # print("\n")
            mm[i][word[j]] = weight[i][j]
    for i in range(len(word)):
        nn[word[i]] = transformer.idf_[i]


    for i in range(6):
        print(i)
        keee = sorted(mm[i].items(), key=lambda item: -item[1])
        n = 10
        for j in keee:
            if (n == 0):
                break
            print(j)
            print()
            n -= 1
    # pd.to_pickle(tfidf, "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/mm_idf.pkl")
    pd.to_pickle(nn, "/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/nn_idf.pkl")

def checkCount2():
    mm = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/mm_tfidf.pkl")
    temp = []
    temp2 = []
    temp1 = []
    temp3 = []
    temp4 = []
    temp5 = []

    for i in range(6):
        print(i)
        keee = sorted(mm[i].items(), key=lambda item: -item[1])
        n = 10
        for j in keee:
            if (n == 0):
                break
            print(j[0]," ",j[1])
            n -= 1

    print(" ".join(temp[3:-1]))


def checkCount3():
    mm = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/nn_idf.pkl")

    keee = sorted(mm.items(), key=lambda item: item[1])
    n = 10
    for j in keee:
        if (n == 0):
            break
        print(j[0]," ",j[1])
        n -= 1


if __name__ == '__main__':
    # getList("wechat_all")
    printCount()
    # checkCount3()

    # getGroupSeriesSmall()
    # howMany()
    # getGroupSeriesSmallSmall()













