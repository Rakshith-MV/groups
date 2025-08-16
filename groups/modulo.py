from functools import cache
import math
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
        self._elements = [elementsA(i,n) for i in range(n)]
        self._identity = 0
        self._inverses = dict(zip(self._elements,
                                   [0]+[self._elements[n-i] for i in range(1,n)])
                                   )
        self._maps = dict(zip(self._elements,range(self._order)))
        print("entering generators")
        self.update_graph(generators=generators)

    def update_graph(self,
                    generators:list):
        """
        1 is always a generator
        """
        self.generators = generators
        self.edges = {}
        for i in self._elements:
            self.edges[self._maps[i]] = [self._maps[(i*j)._number] for j in self.generators]
        self.vertices = circle(self._order)

@cache
class elementsA(element):
    def __init__(self,
                 element,
                 order
                 ):
        self._number = element
        self._gorder = order
        self._order = math.gcd(element, order)
        if self._order == 1 and element != 0:
            self._order = order

    def __mul__(self,
                other):
        if not isinstance(other, element):
            return elementsA((self._number + other)%self._gorder, self._gorder)
        return elementsA((self._number + other._number)%self._gorder, self._gorder)

class ModuloM(Group):
    def __init__(self,
                n:int,
                generators:list=[]
                ):
        temp = unitary(n)
        print(temp)
        self._elements = [elementsM(i,len(temp)) for i in temp]
        self._order = len(temp)
        self._identity = 1
        self._maps = dict(zip(self._elements, range(self._order)))
        self._inverses = {}
        for i in self._elements:
            self._inverses[i] = self.inverse(i)
        self.update_graph(generators=generators)
        

    def inverse(self,
                element):
        i = element
        order = 1
        while(i._number != 1):
            i*=element
            order +=1
        element._order = order
        return i

    def update_graph(self,
                     generators):
        self.generators = generators
        self.edges = {}
        for i in self._elements:
            self.edges[self._maps[i]] = [self._maps[(i*j)._number] for j in self.generators]
        self.vertices = circle(self._order)

@cache
class elementsM(element):
    def __init__(self,
                 element,
                 order
                ):
        self._number = element
        self._gorder = order

    def __mul__(self,
                other):
        if not isinstance(other, element):
            return elementsM((self._number * other)%self._gorder, self._gorder)
        return elementsM((self._number * other._number)%self._gorder, self._gorder)
    
def test():
    k = ModuloA(5)
    for i in k:
        print(i, end=' ')
        print(k._inverses[i])
    print(k.edges)