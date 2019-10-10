#!/user/bin/env python3
# -*- coding: utf-8 -*-
#@file: A_star_in8number.py
#@author: ZHAO Wenzong
#@contact: wenzong_zhao@163.com
#@time: 2019/10/9 21:43
import copy
import time
class Node(object):
    def __init__(self,new_id,father=None):
        self.father=father
        self.__h=0
        self.__g=0
        self.__id=new_id
        self.set_g()
        self.set_h()

    @property
    def h(self):
        return self.__h

    @property
    def g(self):
        return self.__g

    @property
    def f(self):
        return self.__g+self.__h

    @property
    def id(self):
        return self.__id

    def set_g(self):
        if self.father:
            self.__g=self.father.g+1

    def set_h(self):
        end_id = "123804765"
        self.__h=0
        for i in range(len(self.id)):
            if self.id[i]!=end_id[i]:
                self.__h+=1

    def _print(self):
        print 'this state is'
        x=0
        for i in range(3):
            for j in range(3):
                print self.id[x] ,
                x+=1
            print

class A(object):
    def __init__(self,startNode,endNode):
        self.openlist={}
        self.closedlist=set()
        self.startNode=startNode
        self.endNode=endNode
        self.path=[]
        self.expandNum=0
        self.g_dict_shifts = {0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
                         3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
                         6: [3, 7], 7: [4, 6, 8], 8: [5, 7]}

    def getminF(self):
        _min=float('inf')
        _min_id='00000000'
        for pos,node in self.openlist.items():
            if node.f<_min:
                _min=node.f
                _min_id=pos
        return _min_id

    def has_solution(self):
        start=map(int,list(self.startNode.id))
        end=map(int,list(self.endNode.id))
        s_tao=0
        e_tao=0
        for i in range(len(start)):
            if start[i]==0:
                continue
            for j in range(i):
                if start[j]>start[i]:
                    s_tao+=1
        for i in range(len(end)):
            for j in range(i):
                if end[j]>end[i]:
                    e_tao+=1
            if end[i]==0:
                continue
        return e_tao%2 == s_tao%2


    def change_chr(self,s,i,j):
        if i>j:
            i,j=j,i
        new_s=s[:i]+s[j]+s[i+1:j]+s[i]+s[j+1:]
        return new_s

    def expand(self,node):
        self.expandNum+=1
        print 'expand',node.id,self.expandNum,len(self.openlist)
        self.closedlist.add(node.id)
        pos = node.id.find('0')
        for nex_pos in self.g_dict_shifts[pos]:
            child_id = self.change_chr(node.id, pos, nex_pos)
            if child_id in self.closedlist:
                continue
            if child_id not in self.openlist:
                child = Node(child_id, node)
                self.openlist[child_id] = child
            else:
                old_node=self.openlist[child_id]
                child=Node(child_id,node)
                if child.f<old_node.f:
                    self.openlist[child_id] = child

    def find_path(self):
        if not self.has_solution():
            print 'no solution!'
            exit(2)
        self.openlist[self.startNode.id]=self.startNode
        while self.openlist:
            minid=self.getminF()
            node=self.openlist.pop(minid)
            if minid==self.endNode.id:
                print 'find the path!'
                print 'need......',node.g,'step'
                self.mark_path(node)
                break
            self.expand(node)

    def mark_path(self,node):
        if node.father ==None:
            return
        self.path.append(node.id)
        self.mark_path(node.father)

if __name__=="__main__":
    s=Node("836752104")
    e=Node("123804765")
    start_time=time.clock()
    Astar=A(s,e)
    s._print()
    Astar.find_path()
    end_time=time.clock()
    print 'run time',end_time-start_time
    print Astar.path













