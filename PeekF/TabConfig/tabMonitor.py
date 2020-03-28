
import treelib
import re
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

def readPeefF(funcglobe,f1="/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/screenshot_trace_fixed.txt"):
    bigbigText = {"total": 0,'rows':[]}
    # bigbigText = ["funcname","|-dll.funcname|",type,type]

    f = open(f1)
    identifier = 0
    all_info = retFuncinfo()
    print("--------1------")
    lines = f.readlines()
    bigger = []
    parent = []
    parent.append(0)
    linenum = 0
    indent = ['|']
    index = 0
    ret_index = []
    linenum = 0
    # lines1 = lines[:int((len(lines)+1)/100)]
    # lines2 = lines[:int((len(lines)+1)/2):]
    lines1 = lines[0:100]
    indextheirRet = dict()
    bigbigText['total'] = len(lines1)


    for line in tqdm(lines):
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
            if(len(ret_index) == 0):

                bigger.append({'threadn':threadn,'nameshow':nameshow,'inputval':inputvar,'retvar':'','inputtype':all_info[funcname][0],'rettype':all_info[funcname][1],
                               'group':all_info[funcname][2],'file':all_info[funcname][3],'childnum':'','id':str(index),'pid':''})
            else:
                bigger.append({'threadn':threadn,'nameshow':nameshow,'inputval':inputvar,'retvar':'','inputtype':all_info[funcname][0],'rettype':all_info[funcname][1],
                               'group':all_info[funcname][2],'file':all_info[funcname][3],'childnum':'','id':str(index),'pid':str(ret_index[-1])})

                # nameshow inputval retval inputtype rettype group file childnum  id pid

            if (funcname == 'RegisterClassW'):
                ccc = 1




            indextheirRet[index] = 0
            ret_index.append(index)
            index += 1
            # indent.append('-')

        elif "RET" in line:
            linenum += 1
            dllname = ''
            funcname = ''

            retvar = ''

            try:
                dllname = line.split(' ')[1].split('_')[2].split(".")[0].strip()
                funcname = line.split(' ')[1].split('_')[2].split(".")[1].strip()
                retvar = line.split(' ')[1].split('_')[3].strip()

                # thisone = (str(p2.findall(line)[0]).strip().split('.')[0].lower() )

            except IndexError:
                print(line)
                print('---33')
                pause = input()

            if funcname not in funcglobe:
                continue

            # try:
            #     indent.pop()
            # except IndexError:
            #     print(linenum)
            #     print('333333')
            #     for i in bigger:
            #         print(i[2])
            #     input()

            bigger[ret_index[-1]]['retvar'] = retvar
            # if(funcname == 'RegisterClassW'):
            #     input()

            bigger[ret_index[-1]]['childnum'] = str(indextheirRet[ret_index[-1]])

            indextheirRet.pop(ret_index[-1])

            for i in indextheirRet.keys():
                indextheirRet[i] += 1

            try:
                ret_index.pop()
            except IndexError:
                print(linenum)
                for i in bigger:
                    print(i[2])
                input()

    bigbigText['rows'] = bigger[0:100]
    # pd.to_pickle(bigger,"/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_bigger1.pkl")
    pd.to_pickle(bigbigText,"/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_bigbigText1.pkl")

    # return bigger
    # f = open('/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/bigger.txt', 'w')
    #
    # for i in bigger:
    #     f.write(str(i))
    #     f.write('\n')
    # f.close()
    # print(bigger)



def retFilterFunc():
    f = open("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/strip_funcname.txt")
    lines = f.readlines()
    info = []
    alldlls = dict()
    for i in lines:
        funcname = i.split()[0]
        dllname = i.split()[1]
        # print(funcname,dllname)
        if dllname not in alldlls.keys():
            alldlls[dllname] = []

        alldlls[dllname].append(funcname)
        # info.append(funcname)

    return alldlls


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
                arr = [i.var_type, i.ret_type, d+'.c',""]
            # print(arr)
        # print('4')

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
        else:
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

if __name__ == '__main__':
    # m,funcglobe = retFilterFunc()
    # print(funcglobe)

    funcglobe = ['IsTextUnicode', 'InitCommonControlsEx', 'PrivateExtractIconsW', 'ImageList_CoCreateInstance', 'CreateFontIndirectW', 'GetDeviceCaps', 'CreatePatternBrush', 'CreateSolidBrush', 'GetStockObject', 'CreateRectRgn', 'CreateICA', 'CreateCompatibleDC', 'CreateDCA', 'CreateCompatibleBitmap', 'GetDIBits', 'DeleteObject', 'TranslateCharsetInfo', 'CreatePalette', 'SelectPalette', 'GetObjectW', 'GetCurrentObject', 'CreateDIBitmap', 'SelectObject', 'SetStretchBltMode', 'SetBkColor', 'SetTextColor', 'GetDIBColorTable', 'StretchDIBits', 'CreateBitmap', 'BitBlt', 'DeleteDC', 'GetTextMetricsW', 'CreateRoundRectRgn', 'GetViewportExtEx', 'GetWindowExtEx', 'GetLayout', 'GetGlyphIndicesW', 'GetTextAlign', 'GetTextCharsetInfo', 'GetClipRgn', 'IntersectClipRect', 'GetMapMode', 'GetObjectType', 'GetObjectA', 'GetOutlineTextMetricsW', 'GetFontData', 'GetTextFaceW', 'ExtSelectClipRgn', 'CreateDIBSection', 'SetDIBits', 'SaveDC', 'GetClipBox', 'CreateRectRgnIndirect', 'ExtTextOutW', 'SetBkMode', 'GetCurrentPositionEx', 'GetBkMode', 'SetTextAlign', 'MoveToEx', 'SelectClipRgn', 'CombineRgn', 'LPtoDP', 'GetRandomRgn', 'GetRegionData', 'GetViewportOrgEx', 'SetICMMode', 'SetMapMode', 'SetViewportOrgEx', 'SetWindowOrgEx', 'SetROP2', 'ModifyWorldTransform', 'GetDCOrgEx', 'StretchBlt', 'RestoreDC', 'GetTextExtentPoint32W', 'TextOutW', 'GetBitmapBits', 'SetBitmapBits', 'CreateICW', 'EnumFontFamiliesExW', 'GetOutlineTextMetricsA', 'Rectangle', 'SetDIBitsToDevice', 'GetTextCharacterExtra', 'CreateFontA', 'RoundRect', 'ExcludeClipRect', 'PatBlt', 'GetPixel', 'GetEnhMetaFileW', 'GetBitmapDimensionEx', 'RealizePalette', 'GdiplusStartup', 'GdipLoadImageFromStream', 'GdipCreateBitmapFromStream', 'GdipGetImagePixelFormat', 'GdipGetImageHeight', 'GdipGetImageWidth', 'GdipBitmapLockBits', 'GdipBitmapUnlockBits', 'GdipDisposeImage', 'GdipCreateBitmapFromScan0', 'GdipGetImageGraphicsContext', 'GdipCreateSolidFill', 'GdipDrawImageRectI', 'GdipDeleteBrush', 'GdipDeleteGraphics', 'GdipCreateFromHDC', 'GdipGetPropertyItemSize', 'GetForegroundWindow', 'GdipSetInterpolationMode', 'GdipCreatePen1', 'GdipDrawRectangleI', 'GdipFillRectangleI', 'GdipCreateFontFromLogfontW', 'GdipDrawString', 'GdipDeleteFont', 'GdipDrawLineI', 'GdipCreateBitmapFromHBITMAP', 'GdipGetImageEncodersSize', 'GdipGetImageEncoders', 'GdipSaveImageToFile', 'GdipCreateBitmapFromFileICM', 'GdipDrawImageRectRectI', 'ImmGetConversionStatus', 'ImmGetContext', 'ImmGetDefaultIMEWnd', 'ImmSetCompositionWindow', 'ImmSetCompositionFontW', 'ImmReleaseContext', 'ImmNotifyIME', 'ImmEnumInputContext', 'GlobalAddAtomW', 'FindAtomW', 'GetThreadPreferredUILanguages', 'GlobalFindAtomW', 'GlobalGetAtomNameW', 'GlobalDeleteAtom', 'FindAtomA', 'GetTimeFormatW', 'GetACP', 'GetCPInfo', 'LCMapStringW', 'GetFileVersionInfoSizeW', 'GetFileVersionInfoW', 'VerQueryValueW', 'CompareStringW', 'IsDBCSLeadByte', 'CharPrevA', 'CharNextA', 'LCMapStringEx', 'GetThreadLocale', 'lstrcmpiA', 'CompareStringOrdinal', 'GetLocaleInfoEx', 'GetSystemDefaultLCID', 'FindResourceW', 'LoadResource', 'SizeofResource', 'LockResource', 'lstrcmpA', 'GetLocaleInfoW', 'CompareStringA', 'CharLowerA', 'lstrcmpW', 'CharPrevW', 'GetSystemDefaultUILanguage', 'GetUserDefaultLCID', 'ConvertDefaultLocale', 'IsValidLocale', 'CharUpperW', 'GetUserDefaultLocaleName', 'GetUserDefaultLangID', 'GetSystemDefaultLangID', 'CharLowerW', 'FreeResource', 'GetUserDefaultUILanguage', 'GetThreadUILanguage', 'EnumResourceNamesExW', 'GetCPInfoExW', 'GetOEMCP', 'RegisterClassW', 'CreateWindowExW', 'GetGUIThreadInfo', 'IsProcessDPIAware', 'GetDC', 'ReleaseDC', 'GetWindowDC', 'IsWindow', 'GetPropW', 'DefWindowProcW', 'GetClassLongW', 'GetWindowLongW', 'SetPropW', 'RegisterWindowMessageW', 'DestroyWindow', 'RemovePropW', 'UnregisterClassW', 'RegisterWindowMessageA', 'SetWindowsHookExW', 'RegisterClassA', 'RegisterClipboardFormatW', 'RegisterClassExW', 'EnumDisplayMonitors', 'GetMonitorInfoA', 'EnumDisplayDevicesA', 'SetTimer', 'CreateWindowExA', 'ChangeWindowMessageFilter', 'DefWindowProcA', 'LoadIconW', 'LoadCursorW', 'GetClassInfoW', 'SetWindowLongW', 'FindResourceExW', 'CallWindowProcW', 'DwmSetWindowAttribute', 'GetClientRect', 'SetWindowPos', 'IsIconic', 'GetKeyboardLayout', 'ChangeWindowMessageFilterEx', 'LoadStringW', 'SetWinEventHook', 'GetWindowThreadProcessId', 'GetFocus', 'SendMessageW', 'KillTimer', 'PostThreadMessageW', 'RegisterTouchWindow', 'GetWindowRect', 'OffsetRect', 'SetWindowRgn', 'GetWindow', 'InvalidateRect', 'MonitorFromWindow', 'GetMonitorInfoW', 'IsRectEmpty', 'IntersectRect', 'DrawTextW', 'SetProcessDPIAware', 'GetWindowRgnBox', 'GetClassNameW', 'GetAncestor', 'MapWindowPoints', 'PostMessageW', 'InternalGetWindowText', 'GetWindowTextW', 'GetWindowInfo', 'IsZoomed', 'SetRectEmpty', 'InflateRect', 'SetRect', 'SendMessageTimeoutW', 'GetTitleBarInfo', 'EnumChildWindows', 'EnumDisplaySettingsW', 'EnumDisplayDevicesW', 'GetQueueStatus', 'PeekMessageW', 'TranslateMessage', 'DispatchMessageW', 'CallMsgFilterW', 'GetParent', 'LoadImageW', 'ShowWindow', 'SetForegroundWindow', 'IsHungAppWindow', 'GetMessageW', 'ScreenToClient', 'GetCursorPos', 'PtInRect', 'GetKeyState', 'SetCursor', 'TrackMouseEvent', 'GetUpdateRect', 'BeginPaint', 'EndPaint', 'EqualRect', 'UpdateLayeredWindow', 'GetIconInfo', 'DestroyIcon', 'SetFocus', 'SetCapture', 'ReleaseCapture', 'GetClassNameA', 'GetShellWindow', 'SendNotifyMessageW', 'MonitorFromRect', 'DrawIconEx', 'CopyImage', 'GetDoubleClickTime', 'GetKeyboardLayoutList', 'RegisterClipboardFormatA', 'HideCaret', 'IsWindowVisible', 'SetLayeredWindowAttributes', 'RegisterHotKey', 'FindWindowW', 'InSendMessageEx', 'IsTouchWindow', 'UnregisterTouchWindow', 'wvsprintfW', 'GetMessageExtraInfo', 'ShowCaret', 'UpdateWindow', 'CreateCaret', 'SetCaretPos', 'GetCaretPos', 'ClientToScreen', 'GetAsyncKeyState', 'ValidateRect', 'DestroyCaret', 'GetDesktopWindow', 'FindWindowA', 'FindWindowExA', 'FillRect', 'GetDCEx', 'BringWindowToTop', 'SwitchToThisWindow', 'WindowFromPoint', 'wsprintfW', 'OpenClipboard', 'EmptyClipboard', 'SetClipboardData', 'CloseClipboard', 'PostMessageA', 'EnumThreadWindows', 'GetActiveWindow', 'GetClipboardData', 'MonitorFromPoint', 'UnregisterHotKey', 'PostQuitMessage', 'UnhookWindowsHookEx', 'UnregisterClassA', 'UnhookWinEvent', 'GetClassInfoExW']
    # readPeefF(funcglobe,"/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/test_monitor.txt")
    readPeefF(funcglobe)
    # funcglobe = ['a','b','c','d']
    # print(funcglobe[])
    # print(funcglobe[int((len(funcglobe)+1)/2):])



    # f = open('/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/bigger.txt','w')

    # for i in bigger:
    #     f.write(i[2]+'\n')
    # f.close()
