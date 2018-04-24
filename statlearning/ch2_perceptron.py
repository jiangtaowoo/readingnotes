# -*- coding: utf-8 -*-
from vector import Vector


#感知机算法1
def perceptron_1(T, eta):
    def p_init(data):
        (X, y) = data
        return (X.zero(), 0)
    def p_loss(data, W, b):
        (X, y) = data
        return y*(W.dotmult(X) + b)
    def p_update(data, W, b, eta):
        (X, y) = data
        return (W+X.scalarmult(eta*y), b+eta*y)
    def p_print(data, W, b):
        (X, y) = data
        print 'W=', W.prettify(), 'b=', b, '\t[', X.prettify(), y, '] PASS' if p_loss(data, W, b)>0 else '] LOSS'
    roundx = 0
    misscnt = len(T)
    #step1. 初始化w0, b0
    (W, b) = p_init(T[0])
    while misscnt:
        misscnt = 0
        roundx += 1
        #step2. 随机选取一个(xi, yi)
        for data in T:
            p_print(data, W, b)
            #step3. 如果 yi*(w.xi + b) <=0, 更新参数
            if p_loss(data, W, b)<=0:
                misscnt += 1
                (W, b) = p_update(data, W, b, eta)
        print '----ROUND %d:\tMISS=%d----\n' % (roundx, misscnt)
    return (W, b)

#感知机算法2
def perceptron_2(T, eta):
    def Gmatrix(T):
        X = [data[0] for data in T]
        G = []
        for Xi in X:
            gi = []
            G.append(gi)
            for Xj in X:
                gi.append( Xi.dotmult(Xj) )
        return G
    def p_loss(T, G, i, alpha, b):
        cdata = T[i]
        s = 0
        for j, data in enumerate(T):
            (X, y) = data
            s += alpha[j]*y*G[j][i]
        s += b
        return cdata[1]*s
    def p_update(data, i, alpha, b, eta):
        (X, y) = data
        alpha[i] = alpha[i] + eta
        b = b + eta*y
        return b
    def p_print(T, G, i, alpha, b):
        (X, y) = T[i]
        print 'alpha=', alpha, 'b=', b, '\t[', X.prettify(), y, '] PASS' if p_loss(T, G, i, alpha, b)>0 else '] LOSS'
    def p_calcw(T, alpha):
        W = T[0][0].zero()
        for i, data in enumerate(T):
            (X, yi) = data
            W = W + X.scalarmult(alpha[i]*yi)
        return W
    roundx = 0
    misscnt = len(T)
    G = Gmatrix(T)
    #step1. 初始化w0, b0
    (alpha, b) = ([0]*misscnt, 0)
    while misscnt:
        misscnt = 0
        roundx += 1
        #step2. 随机选取一个(xi, yi)
        for i, data in enumerate(T):
            p_print(T, G, i, alpha, b)
            #step3. 如果 yi*(SUM(alhpaj*yj*xj).xi + b) <=0, 更新参数
            if p_loss(T, G, i, alpha, b)<=0:
                misscnt += 1
                b = p_update(data, i, alpha, b, eta)
        print '----ROUND %d:\tMISS=%d----\n' % (roundx, misscnt)
    return (p_calcw(T, alpha), b)

if __name__=="__main__":
    T = [(Vector(0.2,0.1),1),(Vector(0.4,0.6),1),
        (Vector(0.5,0.2),1),(Vector(0.7,0.9),-1)]
    #算法1
    (W, b) = perceptron_1(T, 1)
    print W.prettify(4), b
    print '*************************************************************'
    #算法2
    (W, b) = perceptron_2(T, 1)
    print W.prettify(4), b
