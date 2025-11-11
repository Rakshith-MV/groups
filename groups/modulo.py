from functools import cache
import math

import groups
from .Decorators import unitary
from .group_base import Group, element
from .graphs import circle

imaps = {}
maps = {}

class ModuloA(Group):
    def __init__(self,
                 n,
                 generators:list=[1]
                 ):
        super().__init__(n)
        self._order = n
        self._elements = [elementsA(i,n) for i in range(n)]
        self._identity = 0
        self._inverses = dict(zip(self._elements,[self._elements[0]] + self._elements[:0:-1]))
                                #    [0]+[self._elements[n-i] for i in range(1,n)])
        global imaps, maps 
        maps = dict(zip(self._elements,range(self._order)))
        imaps = dict(zip(range(self._order),self._elements))
        self.update_graph(generators=generators)

    def update_graph(self,
                    generators:list):
        """
        1 is always a generator
        """
        self.generators = generators
        self.edges = {}
        for i in self._elements:
            self.edges[maps[i]] = [maps[i*imaps[int(j)]] for j in self.generators]
        self.vertices = circle(self._order)

    def subgroups(self):
        for i in self._elements:
            i.cycles = self.cycles(i)
        
        K = set(range(self._order))
        K.subsets

    def lattice(self):
        ...


@cache
class elementsA(element):
    def __init__(self,
                 element,
                 order
                 ):
        self._number = element
        self._gorder = order
        self._order = int(order/math.gcd(element, order)) 
        
    def __mul__(self,
                other):
        if not isinstance(other, element):
            return imaps[(self._number + other)%self._gorder]
        return imaps[(self._number + other._number)%self._gorder]

class ModuloM(Group):
    def __init__(self,
                n:int,
                generators:list=[]
                ):
        super().__init__(n)
        temp = unitary(n)
        self._elements = [elementsM(i,n) for i in temp]
        self._order = len(temp)
        self._modn = n
        global maps, imaps
        maps = dict(zip(self._elements, temp))
        imaps = dict(zip(temp , self._elements))
        self.gmaps = dict(zip(self._elements, range(self._order)))
        self._identity = imaps[1]        
        
        self._inverses = {self._identity: self._identity}
        for i in self._elements:
            inv = i
            count = 1
            temp = inv
            while inv != self._identity:
                temp = inv
                inv = inv*i
                count += 1
            self._inverses[i] = temp
            self._inverses[temp] = i
            i._order = count
            temp._order = count
        self.update_graph(generators=generators)

    def update_graph(self,
                     generators=['1']):
        self.edges = {}
        self.generators = generators
        for i in self._elements:
            self.edges[self.gmaps[i]] = [self.gmaps[i*imaps[int(j)]] for j in self.generators]
        self.vertices = circle(self._order)


@cache
class elementsM(element):
    def __init__(self,
                 element,
                 order
                ):
        self._number = element
        self.modn = order
        self._order = None

    def __mul__(self,
                other):
        if not isinstance(other, element):
            return imaps[(self._number * other)%self.modn]
        return imaps[(self._number * other._number)%self.modn]