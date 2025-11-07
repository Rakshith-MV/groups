from functools import cache
import math
from .group_base import Group, element
from .graphs import circle

gmaps = {}
class Dihedral(Group):
    def __init__(self,
                order:int,
                generators:list=[]
                ):
        super().__init__(order)
        self._order = order
        self._elements = [members(i, j, order) for i in range(2) for j in range(order//2)] 
        self._generators = []
        self._identity = self._elements[0]

        global gmaps
        gmaps = dict(zip([(i, j) for i in range(2) for j in range(order//2)], self._elements))
        self._maps = dict(zip(self._elements, range(order)))
        self._imaps= dict(zip(range(order), self._elements))   #Not being used anywhere!!!

        self._inverses = {i: i.inverse() for i in self._elements[1:]}
        self._inverses[self._elements[0]] = self._elements[0]
        self.edges = dict(zip(range(order), [[] for _ in range(order)]))
        self.update_graph(generators=generators)

    def update_graph(self,
                    generators:list=['fr0','r1']):
        """
        Update the graph representation of the Dihedral group.
        """
        self._generators.clear()
        self.vertices = [*circle(self._order//2,0.4),*circle(self._order//2,1)]
        for i in generators:
            if 'e' in i.__str__():
                continue
            if 'f' in i.__str__():
                if 'r' in i.__str__():
                    self._generators.append(gmaps[(1,int(i[-1]))])
                else:
                    self._generators.append(gmaps[(1,0)])
            else:
                self._generators.append(gmaps[(0,int(i[-1]))])
        for j in self._generators:
            for inp,out in zip(self._elements,self.cyclesl(j)):
                self.edges[self._maps[inp]].append(self._maps[out])

    def cyclesl(self,j):
        if isinstance(j, element):
            return [i@j for i in self._elements]
        else:
            raise TypeError("Input must be an instance of the element class.")  

@cache
class members(element):
    def __init__(self,
                f:int,
                r:int,
                order:int):
        self.f = f
        self.r = r
        self._gorder = order  #2n
        self._cycle = self._gorder//2
        self._number = (f, r)
        if f == 0:
            if r == 0:
                self._order = 1
            else:
                self._order = self._cycle//math.gcd(r, self._cycle)
        else:
            self._order = 2

    def inverse(self):
        if self.f == 0:
            return gmaps[(self.f, (self._cycle-self.r-1+1))]
        return self
    
    def __mul__(self, other):
        """
        This represents right multiplication.
        So anytime we pick a choice of generators, the right multiplication is used.
        """
        if isinstance(other, element):
            if other.f == 1:
                return gmaps[((self.f + other.f)%2,(self._cycle-self.r+other.r)%self._cycle)]
            return gmaps[(self.f, (self.r+other.r)%self._cycle)]
        else:
            raise("Multiplication with non-member type is not allowed.")

    def __matmul__(self, other):
        """
        perhaps the left mutliplication is not very usefull with handson computation(just b*a), may be helpfull with graphs
        """
        if isinstance(other,element):
            if other.f == 1:
                return gmaps[((self.f + other.f)%2,(self._cycle-other.r+self.r)%self._cycle)]
            return gmaps[(self.f, (self.r+other.r)%self._cycle)]


    def __str__(self) -> str:
        if self.r != 0:
            return f"fr^{self.r}" if self.f == 1 else f"r^{self.r}"  
        return "f" if self.f == 1 else "e"


def test():
    d = Dihedral(4, ['fr0', 'r1'])
    for i in d:
        print(d._inverses[i], end=' ')
        print(i._order)