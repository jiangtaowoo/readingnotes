# -*- coding: utf-8 -*-
import math
from vector import Vector


class NaiveBayesClassify(object):
    def __init__(self):
        self._I_yc = {}
        self._I_yc_xi = {}
        self._p_yc = {}
        self._p_yc_xi = {}
        self._plambda_yc = {}
        self._plambda_yc_xi = {}

    def training(self, T):
        #贝叶斯估计参数, 默认取值1.0
        lambdap = 1.0
        self._calc_prop(T, lambdap)

    #type=1, 极大似然估计; type=2,贝叶斯估计
    def predict(self, vec, type=1):
        p_yc = self._p_yc if type==1 else self._plambda_yc
        p_yc_xi = self._p_yc_xi if type==1 else self._plambda_yc_xi
        dim = vec.dimension()
        PX = dict()
        for ck, prop in p_yc.iteritems():
            PX[ck] = prop
            for j in xrange(dim):
                Xj = vec[j]
                PX[ck] = PX[ck]*p_yc_xi[ck][j][Xj]
        maxp = 0
        maxck = None
        for k, v in PX.iteritems():
            if v>maxp:
                maxck = k
                maxp = v
        return (maxck, maxp)

    def _calc_prop(self, T, lambdap=1.0):
        dim = T[0][0].dimension()
        N = len(T)
        I_yc = {}
        I_yc_xi = {}
        for (x_vec, y) in T:
            if y in I_yc:
                I_yc[y] += 1
            else:
                I_yc[y] = 1
                I_yc_xi[y] = {i:dict() for i in xrange(dim)}
            for i in xrange(dim):
                xi = x_vec[i]
                if xi in I_yc_xi[y][i]:
                    I_yc_xi[y][i][xi] += 1
                else:
                    I_yc_xi[y][i][xi] = 1
        self._I_yc = I_yc
        self._I_yc_xi = I_yc_xi
        self._calc_prop_type1(N, dim)
        self._calc_prop_type2(N, dim, lambdap)

    def _calc_prop_type1(self, N, dim):
        self._p_yc = {k: 1.0*v/N for k,v in self._I_yc.iteritems()}
        self._p_yc_xi = {k:dict() for k in self._I_yc.keys()}
        for k, v in self._I_yc_xi.iteritems():
            self._p_yc_xi[k] = {i:dict() for i in xrange(dim)}
            for j in xrange(dim):
                vv = v[j]
                for kx, vx in vv.iteritems():
                    self._p_yc_xi[k][j][kx] = 1.0*vx/self._I_yc[k]

    def _calc_prop_type2(self, N, dim, lambdap = 1.0):
        K = len(self._I_yc)
        self._plambda_yc = {k: (1.0*v+lambdap)/(N+K*lambdap) for k,v in self._I_yc.iteritems()}
        self._plambda_yc_xi = {k:dict() for k in self._I_yc.keys()}
        for k, v in self._I_yc_xi.iteritems():
            self._plambda_yc_xi[k] = {i:dict() for i in xrange(dim)}
            for j in xrange(dim):
                vv = v[j]
                Sj = len(vv)
                for kx, vx in vv.iteritems():
                    self._plambda_yc_xi[k][j][kx] = (1.0*vx+lambdap)/(self._I_yc[k] + Sj*lambdap)


T = [(Vector(1,"S"),-1),(Vector(1,"M"),-1),
     (Vector(1,"M"),1),(Vector(1,"S"),1),
     (Vector(1,"S"),-1),(Vector(2,"S"),-1),
     (Vector(2,"M"),-1),(Vector(2,"M"),1),
     (Vector(2,"L"),1),(Vector(2,"L"),1),
     (Vector(3,"L"),1),(Vector(3,"M"),1),
     (Vector(3,"M"),1),(Vector(3,"L"),1),(Vector(3,"L"),-1)]
x = Vector(2,"S")

bayes = NaiveBayesClassify()
bayes.training(T)
(ck, p) = bayes.predict(x)
print x.prettify(), ck, '{:.8f}'.format(p)
print "***********************************"

ck, p = bayes.predict(x, 2)
print x.prettify(), ck, '{:.8f}'.format(p)
print "***********************************"
