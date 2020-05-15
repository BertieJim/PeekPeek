
import numpy as np
from scipy.spatial.distance import euclidean

from fastdtw2 import fastdtw
from tqdm import tqdm

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

'''
test1:
没有树形结构的整体dtw
因为一些树形并不完美，函数的位置并不出于树形的正确位置：一些二级函数未被apimonitor捕捉

问题：会将非同一序列的集合在一起匹配掉

test2:
对一级目录下子树进行匹配
x y 位置
'''

def getLongTrace_nostructure(funcglobe,labledict,f1="/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/screenshot_trace_fixed_0009.txt"):

    f = open(f1)
    identifier = 0
    print("--------1------")
    lines = f.readlines()
    bigger = []
    dllname = ''
    for line in tqdm(lines):

        if "CALL" in line:
            try:
                dllname = line.split(' ')[1].split('_')[2].split(".")[0].strip()
                funcname = line.split(' ')[1].split('_')[2].split(".")[1].strip()
            except IndexError:
                print(line)
                print('iii1')
            if funcname not in funcglobe:
                continue

            nameshow =  labledict[dllname.lower()][funcname.lower()]

            bigger.append(nameshow)
        elif "RET" in line:
            pass
    return np.array(bigger)

def getLongTrace_sectree(funcglobe,labledict,f1="/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/screenshot_trace_notfixed_0009.txt"):
    root_list = BigBigtext.objects.filter(threadn=ed_thread, nameshow='user32.DispatchMessageW')
    all_list = []
    head_id = []
    for i in root_list:
        # if(i.id != 186332):
        #     continue
        each_list = BigBigtext.objects.filter(threadn=ed_thread, pid=i.id)
        temp_list = []
        for j in each_list:
            temp_list.append(labledict[j.nameshow.split('.')[0]][j.nameshow.split('.')[1].lower()])
        all_list.append([i.id,temp_list])
    return all_list


def getLabel(allfunc,dll,baseNum = 3000):
    #TODO:返回一个字典 格式为 dll名称，fun名称 检索
    dllbaselabel = dict()
    dllnum = len(dll)
    base = 0
    for i in dll:
        dllbaselabel[i] = base
        base += baseNum

    dllfunclabel = dict()
    for i in allfunc:
        basenum = dllbaselabel[i]
        basenum2 = 0
        smalldict = dict()

        for j in allfunc[i]:
            smalldict[j] = basenum2 + basenum
            basenum2 += 1
        dllfunclabel[i] = smalldict
    return dllfunclabel

def getKeyTrace(lable_dict,func_):
    x = np.array(['2','3','2','5','0'])
    y = np.array(['3','5','0'])
    f = open("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/keytrace2.txt")
    lines = f.readlines()
    keytrace = []
    longtrace = []
    for line in lines:
        temp = line.split(' ')[2].lower()
        keytrace.append(lable_dict[temp.split('.')[0]][temp.split('.')[1]])
    x = np.array(keytrace)
    return keytrace



if __name__ == '__main__':
    f = open("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/strip_funcname.txt")
    lines = f.readlines()
    alldlls = set()
    allfuncsindll = dict()
    allfuncs = []
    for i in lines:
        funcname = i.split()[0]
        dllname = i.split()[1]
        alldlls.add(dllname.lower())
        allfuncs.append(funcname.lower())
        if(dllname.lower() in allfuncsindll.keys()):
            allfuncsindll[dllname.lower()].append(funcname.lower())
        else:
            allfuncsindll[dllname.lower()] = [funcname.lower()]

    lable_dict = getLabel(allfuncsindll,alldlls)

    long_traces = getLongTrace_sectree(funcglobe,lable_dict)
    key_trace =  getKeyTrace(lable_dict,allfuncs)
    # print(long_trace[0:5])
    #
    print(len(long_traces))
    biggest = 0
    longgest = []
    idest = 0
    for id,long_trace in long_traces:

        distance, path = fastdtw(key_trace, long_trace,  radius=100,dist=lambda x,y:0 if x == y else 100)
        print(distance)

        biggest_temp = len(path)
        if(biggest_temp > biggest):
            biggest = biggest_temp
            longgest = path
            idest = id

    print(longgest)
    print(biggest)
    print(idest)


    # print(distance)
    # f = open("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/fastdtw_res.txt",'w')
    # f.write(str(distance))
    # f.write(str(path))
    # f.close()