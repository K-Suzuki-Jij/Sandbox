# The following code is from 
# https://qiita.com/hiro949/items/d202f748ec87ed3806b2

import numpy as np
from tqdm import tqdm

class Strum():
    def __init__(self,th):
        #実数の探索なので閾値を決める
        self.th = th

    #スツルム列の符号の変化回数を数える
    def sign_flip(self, x:float, n:int, a:list, b:list):
        mm = 1e+64
        cnt = 0
        p0  = 1
        p1  = (x - a[0])
        for i in range(0, n - 1):
            #小行列式の漸化式
            p2 = (x - a[i+1])*p1 - b[i]*b[i]*p0
            #print(p0, p1, p2)
            if (p0 < 0 and p1 > 0) or (p0 > 0 and p1 < 0):
                cnt += 1
            #正->0->負/負->0->正だった場合
            elif abs(p1) < self.th and ((p0 < 0 and p2 > 0) or (p0 > 0 and p2 < 0)):
                cnt += 1
            if i < n - 2:
                p0=p1
                p1=p2
            #p0 = p0/abs(p0)
            #p1 = p1/abs(p1)
            p1 = p1/p0
            p0 = 1
            #print(p0, p1, p2)
        #最後の端の部分
        if (p1 < 0 and p2 > 0) or (p1 > 0 and p2 < 0):
            #print(p1, p2)
            cnt += 1
        return cnt

    def bis(self,n:int,a:list,b:list):
        #固有値の範囲を求める (Gershgorin)
        lim0 = +np.infty
        lim1 = -np.infty
        for i in range(0, n - 2):
            lim0 = min(lim0, a[i+1] - (b[i] + b[i+1]))
            lim1 = max(lim1, a[i+1] + (b[i] + b[i+1]))
        eig_arr = np.array([lim1])
        #i番目に大きい固有値を二分探索で大きい順に求める
        #上限の値はi-1番目に大きい固有値を使えばよい
        for i in tqdm(range(n)):
            ii = n - 1 - i
            x0 = lim0
            x1 = lim1
            pp = 1.0
            while x1 - x0 > self.th:
                pp = x1 - x0
                piv = (x0 + x1)*0.5
                w = self.sign_flip(piv, n, a, b)
                if w <= ii:
                    x1 = piv
                else: 
                    x0 = piv
                if pp - (x1 - x0) < self.th:
                    break
                #print(pp - (x1 - x0))
            eig_arr = np.append(eig_arr, (x1 + x0)*0.5)
            #print(x1)
        return eig_arr[1:]

    def bis_ith(self, x: int, n:int, a:list, b:list):
        x = n - 1 - x
        lim0 = +np.infty
        lim1 = -np.infty
        for i in range(0, n - 2):
            lim0 = min(lim0, a[i+1] - (b[i] + b[i+1]))
            lim1 = max(lim1, a[i+1] + (b[i] + b[i+1]))
        x0 = lim0
        x1 = lim1
        pp = 1.0
        while x1 - x0 > self.th:
            pp = x1 - x0
            piv = (x0 + x1)*0.5
            w = self.sign_flip(piv, n, a, b)
            if w <= x:
                x1 = piv
            else: 
                x0 = piv
            if pp - (x1 - x0) < self.th:
                break
        return (x1 + x0)*0.5

def tridiag(n,a,b):
    mat = np.diag(a)
    for i in range(n-1):
        mat[i][i+1]=b[i]
        mat[i+1][i]=b[i]
    return mat