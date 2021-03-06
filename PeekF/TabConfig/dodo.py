

import treelib
import re
import random
from treelib import Tree, Node
from tqdm import tqdm
import pandas as pd
import sys
import sys
import numpy as np
import os
import django
sys.setrecursionlimit(100000)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PeekPeek.settings")
django.setup()
from PeekF.models import *

not_thread = '0009'
ed_thread = '0009'
def printit(ed_root):

    print(str(ed_root.processn)+str(ed_root.id)
    +" "+str( ed_root.nameshow)
    +" "+str(ed_root.linenum)
    +" "+str(ed_root.childnum)
    +" "+str(ed_root.rettype)
    +" "+str(ed_root.retval)
    +" "+str(ed_root.inputtype)
    +" "+str(ed_root.inputval)
    +" "+str(ed_root.file)
    +" "+str(ed_root.pid)
    +" "+str(ed_root.group))

def retFuncinfo():
    f = open("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/strip_funcname.txt")
    lines = f.readlines()
    alldlls = dict()
    func_info = dict()
    for i in lines:
        funcname = i.split()[0]
        dllname = i.split()[1]
        # print(funcname,dllname)
        if dllname not in alldlls.keys():
            alldlls[dllname] = []

        alldlls[dllname].append(funcname)

        result = ClangWineFunc.objects.filter(func_name=funcname)
        result2 = Funcgroup.objects.filter(funcname=funcname)
        arr = ["","","",""]
        # print('3')
        if(len(result) != 1):
            print("wrong1")
            # print(funcname)
            # input()

        else:
            for i in result:
                m = i.file_name
                c = m.split('_')
                d = "/".join(c)
                arr = [i.var_type, i.ret_type, 'dlls/'+d+'.c',""]
            # print(arr)
        # print('4')
        # if(funcname == 'CreateFontIndirectW'):
        #     www = 'www'
        if (len(result2) != 1):
            if(len(result2) == 0):
                funcnew = funcname[:-1]
                result2 = Funcgroup.objects.filter(funcname=funcnew)
                if(len(result2) != 1):
                    print("wrong3")
                    # print(funcname)
                    # input()
            else:
                print("wrong4")
                # print(funcname)
                # input()
        if (len(result2) == 1):
            for i in result2:
                if(i.group0 != None):
                    arr[3] = i.group0
                if (i.group1 != None):
                    arr[3] += '/'+i.group1
                if (i.group2 != None):
                    arr[3] += '/' + i.group2
                if (i.group3 != None):
                    arr[3] += '/' + i.group3
                if (i.group4 != None):
                    arr[3] += '/' + i.group4
                if (i.group5 != None):
                    arr[3] += '/' + i.group5

                # print(arr)
                # input()
        # print('5')


        func_info[funcname] = arr



    return func_info

def readPeefF(funcglobe,f1="/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/screenshot_trace_notfixed_0009.txt"):
    bigbigText = {"total": 0,'rows':[]}
    # bigbigText = ["funcname","|-dll.funcname|",type,type]

    f = open(f1)
    identifier = 0
    all_info = retFuncinfo()
    print("--------1------")
    lines = f.readlines()
    bigger = dict()
    parent = dict()
    # parent.append(0)

    linenum = 0
    indent = ['|']

    index = dict()
    ret_index = dict()
    linenum = 0

    # lines1 = lines[:int((len(lines)+1)/100)]
    # lines2 = lines[:int((len(lines)+1)/2):]
    # lines1 = lines[0:100]
    indextheirRet = dict()
    indextheirRetdict = dict()
    # bigbigText['total'] = len(lines1)


    numnum = 0

    allthread = {}
    for line in tqdm(lines):
        numnum += 1

        if "CALL" in line:

            linenum += 1

            dllname = ''
            funcname = ''
            inputvar = ''
            threadn = ''
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


            nameshow =  str(dllname) + '.' + str(funcname)
            if threadn not in bigger.keys():
                bigger[threadn] = []
            if threadn not in index.keys():
                index[threadn] = 1
            if threadn not in ret_index.keys():
                ret_index[threadn] = []
            if(index[threadn] == 2):
                print(threadn + '----' + str(index[threadn]))

            if(len(ret_index[threadn]) == 0):

                bigger[threadn].append({'threadn':threadn,'nameshow':nameshow,'inputval':inputvar,'retvar':'','inputtype':all_info[funcname][0],'rettype':all_info[funcname][1],
                               'group':all_info[funcname][3],'file':all_info[funcname][2],'childnum':'','id':index[threadn],'pid':0,'linenum':linenum})
            else:
                bigger[threadn].append({'threadn':threadn,'nameshow':nameshow,'inputval':inputvar,'retvar':'','inputtype':all_info[funcname][0],'rettype':all_info[funcname][1],
                               'group':all_info[funcname][3],'file':all_info[funcname][2],'childnum':'','id':index[threadn],'pid':int(ret_index[threadn][-1]),'linenum':linenum})

                # nameshow inputval retval inputtype rettype group file childnum  id pid

            if (funcname == 'RegisterClassW'):
                ccc = 1

            if(threadn not in indextheirRetdict.keys()):
                indextheirRetdict[threadn] = {}



            if str(index[threadn]) not in indextheirRetdict[threadn].keys():
                indextheirRetdict[threadn][str(index[threadn])] = 0
            # indextheirRetdict[threadn][index] = 0
            if threadn not in ret_index.keys():
                ret_index[threadn] = []

            ret_index[threadn].append(str(index[threadn]))
            index[threadn] += 1
            if threadn not in allthread.keys():
                allthread[threadn] = 0

            allthread[threadn] += 1
            # indent.append('-')

        elif "RET" in line:
            linenum += 1
            dllname = ''
            funcname = ''

            retvar = ''
            threadn = ''

            try:
                dllname = line.split(' ')[1].split('_')[2].split(".")[0].strip()
                funcname = line.split(' ')[1].split('_')[2].split(".")[1].strip()
                retvar = line.split(' ')[1].split('_')[3].strip()
                threadn = line.split(':')[0]

                # thisone = (str(p2.findall(line)[0]).strip().split('.')[0].lower() )

            except IndexError:
                print(line)
                print('---33')
                pause = input()

            if funcname not in funcglobe:
                continue


            bigger[threadn][int(ret_index[threadn][-1])-1]['retvar'] = retvar
            if(funcname == 'RegisterClassW' ):
                www = 'www'
            if ( funcname == 'GetWindowThreadProcessId'):
                www = 'www'

            bigger[threadn][int(ret_index[threadn][-1])-1]['childnum'] = str(indextheirRetdict[threadn][ret_index[threadn][-1]])

            indextheirRetdict[threadn].pop(ret_index[threadn][-1])

            for i in indextheirRetdict[threadn].keys():
                indextheirRetdict[threadn][i] += 1

            try:
                ret_index[threadn].pop()
            except IndexError:
                print(linenum)
                for i in bigger[threadn]:
                    print(i[2])
                input()
        print()
        for i in bigger['0009']:
            print(i['nameshow'] +' ' +str(i['pid']))
        input()
        print()



    print(bigger['0009'][0:5])
    input()

    pd.to_pickle(bigger['0009'],"/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_notfix_d0009.pkl")

def takeOne(not_list,key_list):
    a = 0
    b = 0
    pals = []
    a_len = len(not_list)
    # b_len = len(ed_list)
    # input()
    # print(not_list)
    # print(ed_list)
    b_name = key_list.nameshow
    while(1):
        if(a == a_len ):
            break

        a_name = not_list[a].nameshow
        if(a_name == b_name):
            pals.append({'id':not_list[a].id,'id2':key_list.id,'nameshow2':key_list.nameshow,'inputval2':key_list.inputval,'retval2':key_list.retval,'palsnum':0,'state':1})
            if(not_list[a].retval in key_list.retval ):
                pals[-1]['4'] = 0
            else:
                pass
                # print(not_list[a].retval)
                # print(key_list.retval)
                # print("ret val not even")
                # printit(not_list[a])
                # print("\n ")
                # printit(key_list)
                # input()

            # print(str(a)+'/'+str(a_len)+"  "+str(b)+'/'+str(b_len))
            a = a+1
        else:

            #TODO: 所有父亲processn 变成 1000
            # print(a_name +" "+b_name)
            # printit(not_list[a] )
            # print("\n " )
            # printit(ed_list[b])
            # print("not even")
            # input()
            # b = b+1
            a = a+1
            pass
    return pals

def takePal(not_list,key_list):
    a = 0
    b = 0
    pals = []
    a_len = len(not_list)
    b_len = len(key_list)
    # input()
    # print(not_list)
    # print(ed_list)
    while(1):
        # print(a)
        if(a == a_len or b == b_len):
            break
        b_name = key_list[b].nameshow
        a_name = not_list[a].nameshow
        if(a_name == b_name):
            pals.append({'id':not_list[a].id,'nameshow2':key_list[b].nameshow,'inputval2':key_list[b].inputval,'retval2':key_list[b].retval,'palsnum':0,'state':1})
            if(not_list[a].retval in key_list[b].retval ):
                pals[-1]['4'] = 0
            else:
                pass
                # print(not_list[a].retval)
                # print(key_list.retval)
                # print("ret val not even")
                # printit(not_list[a])
                # print("\n ")
                # printit(key_list)
                # input()

            print(str(a)+'/'+str(a_len)+"  "+str(b)+'/'+str(b_len))
            a = a+1
            b = b+1

        else:

            #TODO: 所有父亲processn 变成 1000
            # print(a_name +" "+b_name)
            # printit(not_list[a] )
            # print("\n " )
            # printit(ed_list[b])
            # print("not even")
            # input()
            # b = b+1
            a = a+1

    if(b == b_len):
        print("done one")

        return pals
    elif(b == 0):
        return []
    else:
        print(str(a) + '/' + str(a_len) + "  " + str(b) + '/' + str(b_len))
        return pals


'''
gdi32.GetStockObject 0
gdi32.CreatePalette 0
gdi32.CreateBitmap 0
gdi32.CreateFontIndirectW 0
gdi32.CreateFontIndirectW 0
gdi32.CreateFontIndirectW 0
gdi32.TranslateCharsetInfo 0
gdi32.CreateFontIndirectW 0

'''

def findIt(not_root,ed_root):
    # print(not_root.count())
    # print(ed_root.count())
    # input()

    pals = takePal(not_root, ed_root)
    for i in pals:
        not_roott = originaltext.objects.filter(threadn=not_thread, pid=i['1'])
        ed_roott = BigBigtext.objects.filter(threadn=ed_thread, pid=i['2'])
        if(not_root.count() == 0):
            return
        else:
            findIt(not_roott,ed_roott)


def main():


    not_root = originaltext.objects.filter(threadn=not_thread,pid = 0)
    ed_root = BigBigtext.objects.filter(threadn=ed_thread,pid = 0)

    # ed_root[0].r
    # ed_root = BigBigtext.objects.filter()
    # not_root = BigBigtext.objects.filter()

    # print(not_root.count())
    # print(ed_root.count())
    index = 1
    pals = takePal(not_root, ed_root)

    for i in tqdm(pals):


        not_roott = originaltext.objects.filter(threadn=not_thread, pid=i['1'])
        ed_roott = BigBigtext.objects.filter(threadn=ed_thread, pid=i['2'])
        # print(not_roott.count())
        # print(ed_roott.count())
        if (not_roott.count() == 0):
            continue
        else:
            index = index + 1
            print("Index" + str(index))
            # input()
            takePal(not_roott, ed_roott)



        # for i in ed_root:
        #     print(i.nameshow+str(i.id))
        #     input()

    print(ed_root[0].pid)
    print(not_root[0].pid)

def getTheChild(id):
    not_roott = originaltext.objects.filter(threadn=not_thread, pid=['1'])
def makeKeyTrace():


    f = open("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/keytrace_done")
    lines = f.readlines()
    for line in lines:
        temp = line.split(" ")
        keys = {"pid":temp[0],"id":temp[1],"nameshow":temp[2],"inputvar":temp[3],"retvar":temp[4].strip()}

        t = KeyTrace()
        t.pid = temp[0]
        t.id = temp[1]
        t.nameshow = temp[2]
        t.inputval = temp[3]
        t.retval = temp[4]
        t.save()

def doCompare():
    not_root = originaltext.objects.filter(threadn=not_thread, pid=0)
    key_root = KeyTrace.objects.filter( pid=0)

    index = 1

    pals = takeOne(not_root, key_root[0])
    print(str(index)," have get:",str(len(pals)))
    input()
    palss = {}
    pal_l = []
    # pal_l += pals
    palss_n = 0
    for i in pals:

        not_roott = originaltext.objects.filter(threadn=not_thread, pid=i['id'])
        key_roott = KeyTrace.objects.filter(pid=1)
        # print(not_roott.count())
        # print(ed_roott.count())
        if (not_roott.count() == 0):
            palss[palss_n] = []
            palss[palss_n].append(i)
            palss_n += 1
            continue
        else:

            # print("Index" + str(index))
            # input()
            temp = takePal(not_roott, key_roott)
            if (len(temp) != 0):
                # print(i)
                pal_l = [i]
                pal_l += temp
    not_roott = originaltext.objects.filter(threadn=not_thread, pid=217783)
    key_roott = KeyTrace.objects.filter(pid=5)
    temp = takePal(not_roott, key_roott)
    if (len(temp) != 0):
        # print(i)
        pal_l += temp
    print(pal_l)
    m = 0
    for i in pal_l:
        t = PalPals()
        t.index = m
        t.id = i['id']
        t.nameshow2 = i['nameshow2']
        t.inputval2 = i['inputval2']
        t.retval2 =i['retval2']
        t.palsnum = i['palsnum']
        t.state = i['state']
        t.save()
        m += 1

def takePal2(not_list,key_list):
    a = 0
    b = 0
    pals = []
    a_len = len(not_list)
    b_len = len(key_list)
    # input()
    # print(not_list)
    # print(ed_list)
    while(1):
        # print(a)
        if(a == a_len or b == b_len):
            break
        b_name = key_list[b].nameshow
        a_name = not_list[a].nameshow
        if(a_name == b_name):
            pals.append({'id':not_list[a].id,'nameshow2':key_list[b].nameshow,'inputval2':key_list[b].inputval,'retval2':key_list[b].retval,'palsnum':0,'state':1})
            if(not_list[a].retval in key_list[b].retval ):
                pals[-1]['4'] = 0
            else:
                pass
                # print(not_list[a].retval)
                # print(key_list.retval)
                # print("ret val not even")
                # printit(not_list[a])
                # print("\n ")
                # printit(key_list)
                # input()

            print(str(a)+'/'+str(a_len)+"  "+str(b)+'/'+str(b_len))
            a = a+1
            b = b+1

        else:

            #TODO: 所有父亲processn 变成 1000
            print(a_name +" "+b_name)
            # print(not_list[a].nameshow )
            # print("\n " )
            # print(key_list[b].nameshow)
            # print("not even")
            input()
            # b = b+1
            a = a+1

    if(b == b_len):
        print("done one")

        return pals
    elif(b == 0):
        return []
    else:
        print(str(a) + '/' + str(a_len) + "  " + str(b) + '/' + str(b_len))
        return pals

def doCompare2():
    not_root = BigBigtext.objects.filter(threadn=ed_thread, pid=0)
    key_root = KeyTrace.objects.filter( pid=0)

    index = 1

    pals = takeOne(not_root, key_root[0])
    print(str(index)," have get:",str(len(pals)))
    input()
    palss = {}
    pal_l = []
    # pal_l += pals
    palss_n = 0
    for i in pals:

        not_roott = BigBigtext.objects.filter(threadn=ed_thread, pid=i['id'])
        key_roott = KeyTrace.objects.filter(pid=1)
        # print(not_roott.count())
        # print(ed_roott.count())
        if (not_roott.count() == 0):
            palss[palss_n] = []
            palss[palss_n].append(i)
            palss_n += 1
            continue
        else:

            # print("Index" + str(index))
            # input()
            temp = takePal(not_roott, key_roott)
            if (len(temp) != 0):
                # print(i)
                pal_l = [i]
                pal_l += temp

    not_roott = BigBigtext.objects.filter(threadn=not_thread, pid=186344)
    key_roott = KeyTrace.objects.filter(pid=5)
    temp = takePal2(not_roott, key_roott)
    print(temp)
    input()
    if (len(temp) != 0):

        pal_l += temp
    print(pal_l)
    input()
    m = 1
    for i in pal_l:
        t = PalPals2()
        t.index = m
        t.id = i['id']
        t.nameshow2 = i['nameshow2']
        t.inputval2 = i['inputval2']
        t.retval2 =i['retval2']
        t.palsnum = i['palsnum']
        t.state = i['state']
        t.save()
        m += 1
if __name__ == '__main__':
    # doCompare2()
    # makeKeyTrace()
    funcglobe = ['IsTextUnicode', 'InitCommonControlsEx', 'PrivateExtractIconsW', 'ImageList_CoCreateInstance', 'CreateFontIndirectW', 'GetDeviceCaps', 'CreatePatternBrush', 'CreateSolidBrush', 'GetStockObject', 'CreateRectRgn', 'CreateICA', 'CreateCompatibleDC', 'CreateDCA', 'CreateCompatibleBitmap', 'GetDIBits', 'DeleteObject', 'TranslateCharsetInfo', 'CreatePalette', 'SelectPalette', 'GetObjectW', 'GetCurrentObject', 'CreateDIBitmap', 'SelectObject', 'SetStretchBltMode', 'SetBkColor', 'SetTextColor', 'GetDIBColorTable', 'StretchDIBits', 'CreateBitmap', 'BitBlt', 'DeleteDC', 'GetTextMetricsW', 'CreateRoundRectRgn', 'GetViewportExtEx', 'GetWindowExtEx', 'GetLayout', 'GetGlyphIndicesW', 'GetTextAlign', 'GetTextCharsetInfo', 'GetClipRgn', 'IntersectClipRect', 'GetMapMode', 'GetObjectType', 'GetObjectA', 'GetOutlineTextMetricsW', 'GetFontData', 'GetTextFaceW', 'ExtSelectClipRgn', 'CreateDIBSection', 'SetDIBits', 'SaveDC', 'GetClipBox', 'CreateRectRgnIndirect', 'ExtTextOutW', 'SetBkMode', 'GetCurrentPositionEx', 'GetBkMode', 'SetTextAlign', 'MoveToEx', 'SelectClipRgn', 'CombineRgn', 'LPtoDP', 'GetRandomRgn', 'GetRegionData', 'GetViewportOrgEx', 'SetICMMode', 'SetMapMode', 'SetViewportOrgEx', 'SetWindowOrgEx', 'SetROP2', 'ModifyWorldTransform', 'GetDCOrgEx', 'StretchBlt', 'RestoreDC', 'GetTextExtentPoint32W', 'TextOutW', 'GetBitmapBits', 'SetBitmapBits', 'CreateICW', 'EnumFontFamiliesExW', 'GetOutlineTextMetricsA', 'Rectangle', 'SetDIBitsToDevice', 'GetTextCharacterExtra', 'CreateFontA', 'RoundRect', 'ExcludeClipRect', 'PatBlt', 'GetPixel', 'GetEnhMetaFileW', 'GetBitmapDimensionEx', 'RealizePalette', 'GdiplusStartup', 'GdipLoadImageFromStream', 'GdipCreateBitmapFromStream', 'GdipGetImagePixelFormat', 'GdipGetImageHeight', 'GdipGetImageWidth', 'GdipBitmapLockBits', 'GdipBitmapUnlockBits', 'GdipDisposeImage', 'GdipCreateBitmapFromScan0', 'GdipGetImageGraphicsContext', 'GdipCreateSolidFill', 'GdipDrawImageRectI', 'GdipDeleteBrush', 'GdipDeleteGraphics', 'GdipCreateFromHDC', 'GdipGetPropertyItemSize', 'GetForegroundWindow', 'GdipSetInterpolationMode', 'GdipCreatePen1', 'GdipDrawRectangleI', 'GdipFillRectangleI', 'GdipCreateFontFromLogfontW', 'GdipDrawString', 'GdipDeleteFont', 'GdipDrawLineI', 'GdipCreateBitmapFromHBITMAP', 'GdipGetImageEncodersSize', 'GdipGetImageEncoders', 'GdipSaveImageToFile', 'GdipCreateBitmapFromFileICM', 'GdipDrawImageRectRectI', 'ImmGetConversionStatus', 'ImmGetContext', 'ImmGetDefaultIMEWnd', 'ImmSetCompositionWindow', 'ImmSetCompositionFontW', 'ImmReleaseContext', 'ImmNotifyIME', 'ImmEnumInputContext', 'GlobalAddAtomW', 'FindAtomW', 'GetThreadPreferredUILanguages', 'GlobalFindAtomW', 'GlobalGetAtomNameW', 'GlobalDeleteAtom', 'FindAtomA', 'GetTimeFormatW', 'GetACP', 'GetCPInfo', 'LCMapStringW', 'GetFileVersionInfoSizeW', 'GetFileVersionInfoW', 'VerQueryValueW', 'CompareStringW', 'IsDBCSLeadByte', 'CharPrevA', 'CharNextA', 'LCMapStringEx', 'GetThreadLocale', 'lstrcmpiA', 'CompareStringOrdinal', 'GetLocaleInfoEx', 'GetSystemDefaultLCID', 'FindResourceW', 'LoadResource', 'SizeofResource', 'LockResource', 'lstrcmpA', 'GetLocaleInfoW', 'CompareStringA', 'CharLowerA', 'lstrcmpW', 'CharPrevW', 'GetSystemDefaultUILanguage', 'GetUserDefaultLCID', 'ConvertDefaultLocale', 'IsValidLocale', 'CharUpperW', 'GetUserDefaultLocaleName', 'GetUserDefaultLangID', 'GetSystemDefaultLangID', 'CharLowerW', 'FreeResource', 'GetUserDefaultUILanguage', 'GetThreadUILanguage', 'EnumResourceNamesExW', 'GetCPInfoExW', 'GetOEMCP', 'RegisterClassW', 'CreateWindowExW', 'GetGUIThreadInfo', 'IsProcessDPIAware', 'GetDC', 'ReleaseDC', 'GetWindowDC', 'IsWindow', 'GetPropW', 'DefWindowProcW', 'GetClassLongW', 'GetWindowLongW', 'SetPropW', 'RegisterWindowMessageW', 'DestroyWindow', 'RemovePropW', 'UnregisterClassW', 'RegisterWindowMessageA', 'SetWindowsHookExW', 'RegisterClassA', 'RegisterClipboardFormatW', 'RegisterClassExW', 'EnumDisplayMonitors', 'GetMonitorInfoA', 'EnumDisplayDevicesA', 'SetTimer', 'CreateWindowExA', 'ChangeWindowMessageFilter', 'DefWindowProcA', 'LoadIconW', 'LoadCursorW', 'GetClassInfoW', 'SetWindowLongW', 'FindResourceExW', 'CallWindowProcW', 'DwmSetWindowAttribute', 'GetClientRect', 'SetWindowPos', 'IsIconic', 'GetKeyboardLayout', 'ChangeWindowMessageFilterEx', 'LoadStringW', 'SetWinEventHook', 'GetWindowThreadProcessId', 'GetFocus', 'SendMessageW', 'KillTimer', 'PostThreadMessageW', 'RegisterTouchWindow', 'GetWindowRect', 'OffsetRect', 'SetWindowRgn', 'GetWindow', 'InvalidateRect', 'MonitorFromWindow', 'GetMonitorInfoW', 'IsRectEmpty', 'IntersectRect', 'DrawTextW', 'SetProcessDPIAware', 'GetWindowRgnBox', 'GetClassNameW', 'GetAncestor', 'MapWindowPoints', 'PostMessageW', 'InternalGetWindowText', 'GetWindowTextW', 'GetWindowInfo', 'IsZoomed', 'SetRectEmpty', 'InflateRect', 'SetRect', 'SendMessageTimeoutW', 'GetTitleBarInfo', 'EnumChildWindows', 'EnumDisplaySettingsW', 'EnumDisplayDevicesW', 'GetQueueStatus', 'PeekMessageW', 'TranslateMessage', 'DispatchMessageW', 'CallMsgFilterW', 'GetParent', 'LoadImageW', 'ShowWindow', 'SetForegroundWindow', 'IsHungAppWindow', 'GetMessageW', 'ScreenToClient', 'GetCursorPos', 'PtInRect', 'GetKeyState', 'SetCursor', 'TrackMouseEvent', 'GetUpdateRect', 'BeginPaint', 'EndPaint', 'EqualRect', 'UpdateLayeredWindow', 'GetIconInfo', 'DestroyIcon', 'SetFocus', 'SetCapture', 'ReleaseCapture', 'GetClassNameA', 'GetShellWindow', 'SendNotifyMessageW', 'MonitorFromRect', 'DrawIconEx', 'CopyImage', 'GetDoubleClickTime', 'GetKeyboardLayoutList', 'RegisterClipboardFormatA', 'HideCaret', 'IsWindowVisible', 'SetLayeredWindowAttributes', 'RegisterHotKey', 'FindWindowW', 'InSendMessageEx', 'IsTouchWindow', 'UnregisterTouchWindow', 'wvsprintfW', 'GetMessageExtraInfo', 'ShowCaret', 'UpdateWindow', 'CreateCaret', 'SetCaretPos', 'GetCaretPos', 'ClientToScreen', 'GetAsyncKeyState', 'ValidateRect', 'DestroyCaret', 'GetDesktopWindow', 'FindWindowA', 'FindWindowExA', 'FillRect', 'GetDCEx', 'BringWindowToTop', 'SwitchToThisWindow', 'WindowFromPoint', 'wsprintfW', 'OpenClipboard', 'EmptyClipboard', 'SetClipboardData', 'CloseClipboard', 'PostMessageA', 'EnumThreadWindows', 'GetActiveWindow', 'GetClipboardData', 'MonitorFromPoint', 'UnregisterHotKey', 'PostQuitMessage', 'UnhookWindowsHookEx', 'UnregisterClassA', 'UnhookWinEvent', 'GetClassInfoExW']
    threadn_name = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_allthread.pkl")
    print(threadn_name)
    m = 0
    c = list(threadn_name.keys())
    print(c)
    while(1):
        print(c[m]," ",(threadn_name[c[m]])," ",c[m+1]," ",(threadn_name[c[m+1]])," ",c[m+2]," ",(threadn_name[c[m+2]])," ",
              c[m+3], " ", (threadn_name[c[m+3]]))
        m = m+4


    #
    # readPeefF(funcglobe)