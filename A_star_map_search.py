#!/user/bin/env python3
# -*- coding: utf-8 -*-
#@file: A_star算法.py
#@author: ZHAO Wenzong
#@contact: wenzong_zhao@163.com
#@time: 2019/10/8 19:25


class Node:
    def __init__(self,x,y,father=None):
        self.x=x
        self.y=y
        self.father=father

        self.G = 0
        self.H = 0
        self.F = 0

    def update(self,father,goal):
        if father and goal:
            self.G=self.cal_g2father(father)+father.G
            self.H=self.cal_h2goal(goal.x,goal.y)
            self.F=self.G+self.F
            self.father=father
        else:
            self.G = 0
            self.H = 0
            self.F = 0


    def cal_g2father(self,father):
        x1 = abs(self.x - father.x)
        y1 = abs(self.y - father.y)
        if (x1 == 1 and y1 == 0):
            return 10  # same row
        if (x1 == 0 and y1 == 1):
            return 10  # same col
        if (x1 == 1 and y1 == 1):
            return 14  # cross
        else:
            return 0

    def cal_h2goal(self,goal_x,goal_y):
        return 4*(abs(self.x-goal_x)+abs(self.y - goal_y))


class Astar:
    def  __init__(self,searchMap):
        self.map=searchMap.map
        self.height=len(self.map)
        self.width=len(self.map[0])
        self.S,self.GOAL=searchMap.getSandG()
        self.openlist={}
        self.closedlist=searchMap.block

    def find_minF(self):
        _min=float('inf')
        _minpos=(0,0)
        for pos,node in self.openlist.items():
            if node.F<_min:
                _min=node.F
                _minpos=pos
        return _minpos

    def expand(self,node):
        print '展开节点',node.x,node.y

        self.closedlist[(node.x,node.y)]=node
        xs = (-1, 0, 1, -1, 1, -1, 0, 1)
        ys = (-1, -1, -1, 0, 0, 1, 1, 1)
        for dx,dy in zip(xs,ys):
            new_x=node.x+dx
            new_y=node.y+dy
            if not self.isvalid(new_x,new_y):
                continue
            if (new_x,new_y) in self.closedlist:
                continue

            if (new_x,new_y) not in self.openlist:
                new_node=Node(new_x,new_y,node)
                new_node.update(node,self.GOAL)
                # print self.istarget(new_node)
                # print new_node.x,node.y,new_node.father.x,new_node.father.y
                self.openlist[(new_x,new_y)]=new_node
            else:
                exist_node=self.openlist[(new_x,new_y)]
                now_node=Node(new_x,new_y,node)
                now_node.update(node,self.GOAL)
                if now_node.F<exist_node.F:
                    self.openlist[(new_x, new_y)]=now_node

    def find_path(self):
        self.print_2Dmap()
        self.openlist[(self.S.x,self.S.y)]=self.S
        while self.openlist:
            print '.........',len(self.openlist)
            pos=self.find_minF()
            node=self.openlist.pop((pos[0],pos[1]))
            if self.istarget(node):
                print node.father.x,node.father.y
                self.mark_path(node)
                print 'find the goal point!'
                break
            self.expand(node)
        else:
            print  "can't find the path!"
            self.print_2Dmap()
            exit(2)
        self.print_2Dmap()
        exit(1)

    def istarget(self,node):
        return node.x == self.GOAL.x and node.y == self.GOAL.y

    def isvalid(self, x, y):
        if x < 0 or x >= self.height or y < 0 or y >= self.width:
            return False
        return True

    def print_2Dmap(self):
        print '    Y',
        for i in xrange(len(self.map)):
            print i, '',
        print
        print '  X'
        row = 0
        for l in self.map:
            print '%3d' % row, ' ',  # 打印的结果为3位整数，如果不够三位了，向左边补空格补足.所有的字符存在_2dmap里面
            row = row + 1
            for i in l:
                print i, '',
            print

    # 用于结束之后从终点沿路寻回
    def mark_path(self,node):

        if node.father == None:
            return
        self.map[node.x][node.y] = '#'

        self.mark_path(node.father)

class Map:
    def __init__(self):
        self.map=[]
        self.block={}
        self.map.append('S X . . . . . . . . . . . . . X . . . .'.split())
        self.map.append('. . . . . . . . . . . . . . . X . . . .'.split())
        self.map.append('. X . . . . . . . . . . . . . X . . . .'.split())
        self.map.append('. X . . . . . . . X . . . . . X . . . .'.split())
        self.map.append('. . . . . . . . . X . . . . X X . . . .'.split())
        self.map.append('. . . . . X . . . . . . . . . . . . . .'.split())
        self.map.append('. . . . . . . . X . . . . . . X X X X .'.split())
        self.map.append('. . . . . . . . . . . . . . . X . . . .'.split())
        self.map.append('. . . . . . . . X . . . . . . X E X X X'.split())
        self.map.append('. . . . . . . . X . . . . . . . . . . .'.split())
        self.map.append('. . . . . . . . . . . . . . . . . X . .'.split())
        self.map.append('. . . . . . . . . . . . . . . . . X . .'.split())
        self.map.append('. . . . . . . . . . . . X . . X . X . .'.split())
        self.map.append('. . . . . . . . . . . . . . X X . X . .'.split())
        self.map.append('. . . . . . . . . . . . . . . X . . . .'.split())
        self.map.append('. . . . . . . . . . . . . . . X . X . .'.split())

    def getSandG(self):
        map_border = (len(self.map), len(self.map[0]))
        print 'map_border', map_border
        row_index = 0
        for row in self.map:
            col_index = 0
            for n in row:
                if n == 'X':
                    block_node=Node(row_index, col_index)
                    self.block[(block_node.x, block_node.y)] = block_node
                elif n == 'S':
                    start = Node(row_index, col_index)
                elif n == 'E':
                    end = Node(row_index, col_index)
                col_index = col_index + 1
            row_index = row_index + 1
        return (start,end)

if __name__=='__main__':
    map=Map()
    a=Astar(map)
    a.find_path()






