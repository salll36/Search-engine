from numpy import *


class PageRank:
    def __init__(self, a, p=0.85):
        self.a = a.astype(float)
        self.p = p

    def transPre(self, data):
        # 构造转移矩阵
        b = transpose(data)  # 把矩阵转置
        c = zeros((data.shape), dtype=float)
        # 把所有的元素重新分配
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                c[i][j] = data[i][j] / (b[j].sum())

        return c

    def initiPre(self, c):
        # pr值的初始化
        pr = zeros((c.shape[0], 1), dtype=float)
        for i in range(c.shape[0]):
            pr[i] = float(1) / c.shape[0]
        return pr

    def page_rank(self):
        m = self.transPre(self.a)
        pr = self.initiPre(m)

        # pageRank算法
        while ((pr == self.p * dot(m, pr) + (1 - self.p) * pr).all() == False):
            pr = self.p * dot(m, pr) + (1 - self.p) * pr

        return pr.round(5)