from functools import cache
import math
from .group_base import Group, element
from .graphs import circle

class Dihedral(Group):
    def __init__(self,
                 order:int,
                 generators:list=[]
                 ):
        super().__init__(order)
        self._order = order
        self._elements = [members(i, j, order, self) for i in range(2) for j in range(order//2)] 
        self._generators = []
        self._identity = self._elements[0]

        self.gmaps = dict(zip([(i, j) for i in range(2) for j in range(order//2)], self._elements))
        self._maps = dict(zip(self._elements, range(order)))
        self._imaps = dict(zip(range(order), self._elements))

        self._inverses = {i: i.inverse() for i in self._elements[1:]}
        self._inverses[self._elements[0]] = self._elements[0]
        self.edges = dict(zip(range(order), [[] for _ in range(order)]))
        self.update_graph(generators=generators)

    def update_graph(self,
                     generators:list=['fr0','r1']):
        """
        Update the graph representation of the Dihedral group.
        """
        if generators is None:
            generators = []
        self._generators.clear()
        self.vertices = [*circle(self._order//2,0.4),*circle(self._order//2,1)]
        for gen_item in generators:
            if isinstance(gen_item, members):
                if gen_item._number != (0, 0):
                    self._generators.append(gen_item)
                continue
            s = str(gen_item).strip()
            if s == 'e' or not s:
                continue
            f_val = 1 if 'f' in s else 0
            r_val = 0
            if 'r' in s:
                import re
                m = re.search(r'r\^?(\d+)', s)
                if m:
                    r_val = int(m.group(1)) % (self._order // 2)
                else:
                    r_val = 1 % (self._order // 2)
            if (f_val, r_val) in self.gmaps:
                self._generators.append(self.gmaps[(f_val, r_val)])

        if not self._generators:
            if (0, 1 % (self._order // 2)) in self.gmaps:
                self._generators.append(self.gmaps[(0, 1 % (self._order // 2))])
            if (1, 0) in self.gmaps:
                self._generators.append(self.gmaps[(1, 0)])

        for j in self._generators:
            for inp,out in zip(self._elements,self.cyclesl(j)):
                self.edges[self._maps[inp]].append(self._maps[out])

    def cyclesl(self,j):
        if isinstance(j, element):
            return [i@j for i in self._elements]
        else:
            raise TypeError("Input must be an instance of the element class.")  


class members(element):
    def __init__(self,
                 f:int,
                 r:int,
                 order:int,
                 group=None):
        super().__init__()
        self.f = f
        self.r = r
        self._gorder = order  #2n
        self._cycle = self._gorder//2
        self._number = (f, r)
        self._group = group
        if f == 0:
            if r == 0:
                self._order = 1
            else:
                self._order = self._cycle//math.gcd(r, self._cycle)
        else:
            self._order = 2

    def inverse(self):
        if self.f == 0:
            return self._group.gmaps[(self.f, (self._cycle-self.r))]
        return self
    
    def __mul__(self, other):
        """
        This represents right multiplication.
        So anytime we pick a choice of generators, the right multiplication is used.
        """
        if isinstance(other, element):
            if other.f == 1:
                return self._group.gmaps[((self.f + other.f)%2,(self._cycle-self.r+other.r)%self._cycle)]
            return self._group.gmaps[(self.f, (self.r+other.r)%self._cycle)]
        else:
            raise TypeError("Multiplication with non-member type is not allowed.")

    def __matmul__(self, other):
        """
        perhaps the left mutliplication is not very usefull with handson computation(just b*a), may be helpfull with graphs
        """
        if isinstance(other,element):
            if other.f == 1:
                return self._group.gmaps[((self.f + other.f)%2,(self._cycle-other.r+self.r)%self._cycle)]
            return self._group.gmaps[(self.f, (self.r+other.r)%self._cycle)]


    def __str__(self) -> str:
        if self.r != 0:
            return f"fr^{self.r}" if self.f == 1 else f"r^{self.r}"  
        return "f" if self.f == 1 else "e"