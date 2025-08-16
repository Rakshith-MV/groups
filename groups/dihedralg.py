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
        self._elements = [members(i, j, order) for i in range(2) for j in range(order//2)]
        self._generators = []
        self._identity = members(0, 0, order)
        self._maps = dict(zip([(i, j) for i in range(2) for j in range(order//2)], range(order)))
        self._inverses = {i: i.inverse() for i in self._elements}
        self.edges = dict(zip(range(order), [[] for _ in range(order)]))
        self.update_graph(generators=generators)

    def update_graph(self,
                    generators:list=['fr0','r1']):
        """
        Update the graph representation of the Dihedral group.
        """
        print("Updating Dihedral group graph with generators:", generators)
        self._generators.clear()
        self.vertices = [*circle(self._order//2,0.4),*circle(self._order//2,1)]
        for i in generators:
            if 'e' in i.__str__():
                continue
            if 'f' in i.__str__():
                if 'r' in i.__str__():
                    self._generators.append(members(1,int(i[-1]),self._order))
                else:
                    self._generators.append(members(1,0,self._order))
            else:
                self._generators.append(members(0,int(i[-1]),self._order))
        for j in self._generators:
            for inp,out in zip(self._elements,self.cycles(j)):
                self.edges[self._maps[(inp.f,inp.r)]].append(self._maps[out.f,out.r])

@cache
class members(element):
    def __init__(self,
                f:int,
                r:int,
                order:int):
        self.f = f
        self.r = r
        self._gorder = order
        self._cycle = self._gorder//2
        self._number = (f, r)
        if f == 0:
            if r == 0:
                self._order = 1
            else:
                self._order = math.gcd(r, self._cycle)
        else:
            self._order = math.gcd(r,self._cycle, 2)

    def inverse(self):
        if self.f == 0:
            return members(self.f, (self._cycle-self.r), self._gorder)
        return members(self.f, self.r, self._gorder)
    
    def __mul__(self, other):
        if isinstance(other, element):
            if other.f == 1:
                return members((self.f + other.f)%2,(self._cycle-self.r+other.r)%self._cycle,self._gorder)
            return members(self.f, (self.r+other.r)%self._cycle,self._gorder)    
        else:
            raise("Multiplication with non-member type is not allowed.")

    
    def __str__(self) -> str:
        if self.r != 0:
            return f"fr^{self.r}" if self.f == 1 else f"r^{self.r}"  
        return "f" if self.f == 1 else "e"


def test():
    d = Dihedral(4, ['fr0', 'r1'])
    for i in d:
        print(d._inverses[i], end=' ')
        print(i._order)