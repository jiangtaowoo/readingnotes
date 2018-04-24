# -*- coding: utf-8 -*-
import math
from vector import Vector


#根据中位数, 切分数据
def split_by_mid(nodes, key):
    l = sorted(nodes, key=key)
    i = int(math.ceil((len(l)+1.0)/2)-1)
    tl = l[:i]
    v0 = l[i]
    tr = l[(i+1):]
    return v0, tl, tr

#构造kd树
def kd_tree_build(parent, T, vecdim, depth):
    #tree = [node, cur-dimension, parent, left, right]
    l = depth % vecdim
    (v0, tl, tr) = split_by_mid(T, key=lambda data: data[l])
    node = [v0, l, parent, None, None]
    left = kd_tree_build(node, tl, vecdim, depth+1) if tl else None
    right = kd_tree_build(node, tr, vecdim, depth+1) if tr else None
    node[3] = left
    node[4] = right
    return node

def kd_tree_search(tree, x):
    (vec, l, parent, left, right) = tree
    if left is None and right is None:
        return tree
    if x[l]<vec[l]:
        if left:
            return kd_tree_search(left, x)
        return tree
    if x[l]>=vec[l]:
        if right:
            return kd_tree_search(right, x)
        return tree

def kd_tree_nearest(tree, kzones, x):
    backtraced = []
    distraced = []
    nearest = [None, None]
    kdsearch = True
    zones = map(lambda x: x[0], kzones)
    def backtrace(treenode):
        if treenode not in backtraced:
            backtraced.append(treenode)
            distraced.append(nearest[1])
    def updatenearest(node):
        if node not in zones:
            dis = x.distance(node[0])
            (vec, ndis) = nearest
            if not ndis or dis<ndis:
                nearest[0] = node
                nearest[1] = dis
    while kdsearch or current:
        #step1. 从tree出发, 找到x的最近邻点
        if kdsearch:
            current = kd_tree_search(tree, x)
            updatenearest(current)
            backtrace(current)
            kdsearch = False
        #step2. 回溯
        (nodev, l, parent, left, right) = current
        other = None
        if parent:
            other = parent[3] if parent[4] is current else parent[4]
        #1.父节点: 分割点本身的距离判断
        if parent and parent not in backtraced:
            updatenearest(parent)
            backtrace(parent)
        #2.相邻子节点的距离判断
        if other and other not in backtraced:
            ov, ol = other[0], other[1]
            hyperdis = x.distance_hyperect(ol, ov[ol])
            if hyperdis<nearest[1]:
                #分割超平面与当前最近邻超球体相交
                tree = other
                kdsearch = True
            else:
                current = other[2]
        else:
            #向上回退
            current = parent
    print_search_trace(backtraced, distraced)
    kzones.append(nearest)
    return nearest

def knn(tree, k, x):
    kzones = []
    for i in xrange(0,k):
        kd_tree_nearest(tree, kzones, x)
    return kzones

def print_search_trace(backtraced, distraced):
    for idx, node in enumerate(backtraced):
        kd_node_prettify(node, distraced[idx], '%d:\t' % (idx))

def kd_node_prettify(node, mindis, tips):
    #(vector, l, parent, left, right)
    if node:
        print tips, node[0].prettify(), " split=", node[1], "mindis=", mindis


T = [Vector(2,3),Vector(5,4),
     Vector(9,6),Vector(4,7),
     Vector(8,1),Vector(7,2)]

tree = kd_tree_build(None,T,2,0)
k = 1

x = Vector(3,4.5)
kzones = knn(tree, k, x)
#node, dis = kd_tree_nearest(tree, x)
print "-----------------------------------"
for (node, dis) in kzones:
    print x.prettify(), node[0].prettify(), dis
print "\n***********************************\n"

x = Vector(2,4.5)
kzones = knn(tree, k, x)
#node, dis = kd_tree_nearest(tree, x)
print "-----------------------------------"
for (node, dis) in kzones:
    print x.prettify(), node[0].prettify(), dis
print "\n***********************************\n"

x = Vector(8.5,3)
kzones = knn(tree, k, x)
#node, dis = kd_tree_nearest(tree, x)
print "-----------------------------------"
for (node, dis) in kzones:
    print x.prettify(), node[0].prettify(), dis
