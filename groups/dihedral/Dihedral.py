import math
from functools import cache


"""
2 operations, one cyclic the other flips, 
Rotations and Reflections

say Rotations   = r
    Reflections = f

"""

@cache
class members:
    def __init__(self,
                 f:bool,
                 r:int,
                 n:int
                 ) -> None:
        self.color = 'white'
        self.r = r
        self.f = f
        self.n = n
        self.conjugates = set()
        self.order = 1

    def _cycle_inverse(self,
                      ) -> None:
        o = [self.f, self.r]
        while o != [0,0]:
            o = [(2*o[0])%2, (2*o[1])%self.n]
            self.order +=1
        self.inv = members(*o,self.n)

        """
        In D4
        Elements of order 1: e
        Elements of order 2: r2, f, fr, r2f, rf
        Elements of order 4: r, r3

        In D5 there are 3 order classes. Each is listed here:

        Elements of order 1: e
        Elements of order 2: f, fr, fr2, r2f, rf
        Elements of order 5: r, r2, r3, frf
        
        In D6
        Elements of order 1: e
        Elements of order 2: r3, f, fr, fr2, r3f, r2f, rf
        Elements of order 3: r2, r4
        Elements of order 6: r, frf
        """
        
    def __mul__(self,
                element
                )->any:
        if element.f == 1:
            return members((self.f + element.f)%2,(self.n-self.r+element.r)%self.n,self.n)
        return members(self.f, (self.r+element.r)%self.n,self.n)

    def __eq__(self, value: object) -> bool:
        if self.r != value.r or \
            self.n != value.n or \
                self.f != value.f:
            return 0
        return 1
    
    def __str__(self) -> str:
        return f"f^{self.f}r^{self.r}"  


class Dn:
    def __init__(self,
                 n) -> None:
        self.n = n
        self.elements = [members(i,j,self.n) for i in range(2) for j in range(self.n)]
        self.conjugacy_classes = set()
        self.id = members(0,0,n)
        for i in self.elements:
            i._cycle_inverse()

    def compute_conjugacy_classes(self
                          ):
        for i in self.elements:
            for j in self.elements:
                t = j*i*j.inv
                i.conjugates.append(t) if t not in i.conjugates else None
            self.conjugacy_classes.add(i.conjugates)
        return self.conjugacy_classes



    def cayleys(self
                )->list:
        self.table = []
        for i in self.elements:
            temp = []
            for j in self.elements:
                temp.append(i*j)
            self.table.append(temp)
        return self.table

        
if __name__ == "__main__":
    k = Dn(4)