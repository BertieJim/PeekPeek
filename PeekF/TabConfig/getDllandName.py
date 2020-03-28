
import pandas as pd

def main():
    p = open("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/allDllIntro")
    lines = p.readlines()
    c = dict()
    for line in lines:
        m = line.split(".dll")[0].strip().lower()
        n = line.split(".dll")[1].strip()
        c[m] = n
    dd = dict()

    dllandallfuncs = pd.read_pickle("/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/DLLandFuncNameOnly.pkl")
    for i in dllandallfuncs:
        try:
            tt = (i,c[i.split('.dll')[0].lower()])
        except KeyError:
            # print(i)
            print(str(i).split('.dll')[0].lower())
            input()
            continue
        print('-')

        dd[tt] = dllandallfuncs[i]

    pd.to_pickle(dd,"/Users/bertie/PycharmProjects/PeekPeek/PeekF/data/DLlandInfo.pkl")






if __name__ == '__main__':
    main()