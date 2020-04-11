
import os
import pandas as pd





def main2():
    allfuncandtheirgroup = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/findfuncgroupinonefile.pkl")
    _result = dict()
    _func = []
    for i, dllname in allfuncandtheirgroup:
        if dllname not in _result.keys():
            _result[dllname] = []

        _result[dllname].append(i)

    m = sorted(_result.keys())
    newdict = dict()
    for i in m:
        if i == '*':
            continue
        newdict[i] = _result[i]

    pd.to_pickle(newdict,"/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/DLLandFuncNameOnly.pkl")


def getMakeFile(dir):
    files_ = []
    list = os.listdir(dir)

    for i in range(0, len(list)):

        path = os.path.join(dir, list[i])
        if os.path.isdir(path):
            allFiles = os.listdir(path)
            for i in allFiles:
                suffix = os.path.splitext(i)[1]
                if suffix == '.spec':
                    path = os.path.join(path,i)
                    files_.append(path)

    return files_

def main():
    path = '/Users/bertie/Downloads/wine-5.0/dlls/'
    allMakeFile = getMakeFile(path)
    dllandFunc = dict()
    for i in allMakeFile:
        dllname = os.path.split(i)[-1].split(".")[0]
        # print(dllname)

        f = open(i)
        lines = f.readlines()
        _func = []
        for line in lines:
            funcname = line.strip().split(' ')[-1].split("(")[0]

            _func.append(funcname)
        if dllname not in dllandFunc.keys():
            dllandFunc[dllname] = _func
        print(dllandFunc[dllname])
        input()
    m = sorted(dllandFunc)
    alist = []
    newdict = dict()
    for i in m:
        newdict[i] = dllandFunc[i]
    # dllandallfuncs = {"d1":["f1","f2"],"z1":["f1","f2"],"a1":["f1","f2"]}
    # print(sorted(dllandallfuncs))
    # print(dllandallfuncs)

    pd.to_pickle(newdict,"/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/DLLandFuncNameOnly.pkl")
    # pd.to_pickle(m,"/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/DLLNameOnly.pkl")


def main3():
    allthread = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/monitor_allthread.pkl")
    temp = []
    temp2 = []

    for i in allthread.keys():
        temp.append(i)
    print(" ".join(temp[16:-1]))

    for i in allthread.keys():
        temp2.append(str(allthread[i]))

    print(" ".join(temp2[16:-1]))
    print(len(temp))

if __name__ == '__main__':
    main3()