# The following code is from 
# https://qiita.com/hiro949/items/d202f748ec87ed3806b2

import numpy as np
import math
from tqdm import tqdm

def tridiag(n,a,b):
    mat = np.diag(a)
    for i in range(n-1):
        mat[i][i+1]=b[i]
        mat[i+1][i]=b[i]
    return mat

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
            c1 = (p0 < 0 and p1 > 0) or (p0 > 0 and p1 < 0)

            #正->0->負/負->0->正だった場合
            c2 = abs(p1) < self.th and ((p0 < 0 and p2 > 0) or (p0 > 0 and p2 < 0))
            if c1 or c2:
                cnt += 1
            
            #p0=p1
            #p1=p2
            #p1 = p1/p0
            #p0 = 1

            p1 = p2/p1
            p0 = 1
            #print(p0, p1, p2)
        #最後の端の部分
        if (p0 < 0 and p1 > 0) or (p0 > 0 and p1 < 0):
            #print(p1, p2)
            cnt += 1
        return cnt

    def bis(self,n:int,a:list,b:list):
        #固有値の範囲を求める (Gershgorin)
        lim0 = +np.infty
        lim1 = -np.infty
        for i in range(0, n - 2):
            lim0 = min(lim0, abs(a[i+1]) - (abs(b[i]) + abs(b[i+1])))
            lim1 = max(lim1, abs(a[i+1]) + (abs(b[i]) + abs(b[i+1])))
        eig_arr = np.array([lim1])
        #i番目に大きい固有値を二分探索で大きい順に求める
        #上限の値はi-1番目に大きい固有値を使えばよい
        for i in tqdm(range(n)):
            ii = n - 1 - i
            x0 = lim0
            x1 = lim1
            pp = 1.0
            while abs(x1 - x0) > self.th:
                print(abs(x1 - x0))
                pp = x1 - x0
                piv = (x0 + x1)*0.5
                w = self.sign_flip(piv, n, a, b)
                if w <= ii:
                    x1 = piv
                else: 
                    x0 = piv
                if abs(pp - (x1 - x0)) < self.th:
                    print("fdfsafd")
                    break
            eig_arr = np.append(eig_arr, (x1 + x0)*0.5)
            #print(x1)
        return eig_arr[1:]

    def bis_ith(self, x: int, n:int, a:list, b:list):
        x = n - 1 - x
        lim0 = +np.infty
        lim1 = -np.infty
        for i in range(0, n - 2):
            lim0 = min(lim0, a[i+1] - (abs(b[i]) + abs(b[i+1])))
            lim1 = max(lim1, a[i+1] + (abs(b[i]) + abs(b[i+1])))
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
        
        eig_val = (x1 + x0)*0.5
        
        
        def normalize(vec):
            norm = 0.0
            for i in range(len(vec)):
                norm += vec[i]*vec[i]

            for i in range(len(vec)):
                vec[i] = vec[i]/math.sqrt(norm)

        """
        vec = [1]
        vec.append((eig_val - a[0])/b[0])
        for i in range(0, n - 2):
            c0 = vec[i]
            c1 = vec[i+1]
            c2 = ((eig_val - a[i+1])*c1 - b[i]*c0)/b[i+1]
            vec.append(c2)

        normalize(vec)
        """

        vec = np.random.uniform(-1, 1, n)
        normalize(vec)

        # Inverse Iteration
        delta = 1e-11
        mat = tridiag(n, a - eig_val + delta, b)
        for _ in range(5):
            new_vec = np.linalg.solve(mat, vec)
            normalize(new_vec)
            #print(np.dot(new_vec, vec))
            vec = new_vec

        return eig_val, vec

