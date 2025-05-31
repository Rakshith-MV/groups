from functools import cache
import math
from .group_base import Group, element
from .graphs import circle

class ModuloA(Group):
    def __init__(self,
                 n,
                 generators:list=[]
                 ):
        super().__init__(n)
        self._order = n
        self._elements = [elementsA(i,n) for i in range(n)]
        self._identity = 0
        self._inverses = dict(zip(self._elements,
                                   [0]+[self._elements[n-i] for i in range(1,n)])
                                   )
        self._maps = dict(zip(self._elements,range(self._order)))
        self.update_graph(generators=generators)

    def update_graph(self,
                    generators):
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
                 n:int
                 ):
        self._elements = [elementsM(i,n) for i in range(1,n) if math.gcd(i,n) == 1]
        self._order = len(self._elements)
        self._identity = 1
        self._maps = dict(zip(self._elements, range(self._order)))
        self._inverses = {}
        for i in self._elements:
            self._inverses[i] = self.inverse(i)
        # self.update_graph(generators=generators)
        self.edges = {}
        self.vertices = []


    def inverse(self,
                element):
        for i in self._elements:
            if (i * element)._number == 1:
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
        self._order = order
        
    def __mul__(self,
                other):
        if not isinstance(other, element):
            return elementsM((self._number * other)%self._gorder, self._gorder)
        return elementsM((self._number * other._number)%self._gorder, self._gorder)
    
if __name__ == "__main__":
    k = ModuloM(10)