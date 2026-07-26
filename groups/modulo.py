from functools import cache
import math

import groups
from .Decorators import unitary
from .group_base import Group, element
from .graphs import circle

class ModuloA(Group):
    def __init__(self,
                 n,
                 generators:list=[1]
                 ):
        super().__init__(n)
        self._order = n
        self._elements = [elementsA(i, n, self) for i in range(n)]
        self._identity = self._elements[0]
        self._inverses = dict(zip(self._elements, [self._elements[0]] + self._elements[:0:-1]))
        
        self._maps = dict(zip(self._elements, range(self._order)))
        self._imaps = dict(zip(range(self._order), self._elements))
        self.update_graph(generators=generators)

    def update_graph(self,
                     generators:list):
        self.generators = generators
        self.edges = {}
        for i in self._elements:
            self.edges[self._maps[i]] = [self._maps[i * self._imaps[int(j)]] for j in self.generators]
        self.vertices = circle(self._order)


class elementsA(element):
    def __init__(self,
                 element,
                 order,
                 group=None
                 ):
        super().__init__()
        self._number = element
        self._gorder = order
        self._order = int(order / math.gcd(element, order))
        self._group = group
        
    def __mul__(self,
                other):
        if not isinstance(other, element):
            val = (self._number + other) % self._gorder
        else:
            val = (self._number + other._number) % self._gorder
        return self._group._imaps[val]


class ModuloM(Group):
    def __init__(self,
                 n:int,
                 generators:list=[]
                 ):
        super().__init__(n)
        temp = unitary(n)
        self._elements = [elementsM(i, n, self) for i in temp]
        self._order = len(temp)
        self._modn = n
        
        self._maps = dict(zip(self._elements, temp))
        self._imaps = dict(zip(temp, self._elements))
        self.gmaps = dict(zip(self._elements, range(self._order)))
        self._identity = self._imaps[1]
        
        self._inverses = {self._identity: self._identity}
        for i in self._elements:
            inv = i
            count = 1
            temp_val = inv
            while inv != self._identity:
                temp_val = inv
                inv = inv * i
                count += 1
            self._inverses[i] = temp_val
            self._inverses[temp_val] = i
            i._order = count
            temp_val._order = count
        self.update_graph(generators=generators)

    def update_graph(self,
                     generators=['1']):
        self.edges = {}
        self.generators = generators
        for i in self._elements:
            self.edges[self.gmaps[i]] = [self.gmaps[i * self._imaps[int(j)]] for j in self.generators]
        self.vertices = circle(self._order)


class elementsM(element):
    def __init__(self,
                 element,
                 order,
                 group=None
                 ):
        super().__init__()
        self._number = element
        self.modn = order
        self._order = None
        self._group = group

    def __mul__(self,
                other):
        if not isinstance(other, element):
            val = (self._number * other) % self.modn
        else:
            val = (self._number * other._number) % self.modn
        return self._group._imaps[val]