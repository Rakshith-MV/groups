"""
2 operations, one cyclic the other flips, 
Rotations and Reflections

say Rotations   = r
    Reflections = f

"""


class members:
    def __init__(self,
                 r:int,
                 f:bool,
                 n:int
                 ) -> None:
        self.r = r
        self.f = f
        self.n = n
        self._cycle_inverse()

    def _cycle_inverse(self,
                      ) -> None:
        ...

    def __eq__(self, value: object) -> bool:
        if self.r != value.r or \
            self.n != value.n or \
                self.f != value.f:
            return 0
        return 1

class dihedral:


    def __init__(self,
                 n) -> None:
        self.n = n
        self.init(self.n)
        self.id = members(0,0,n)

    def init(self,
             n) -> None:
        for i in range(n):
            self.elements.append(members(i,0,self.n))
            self.elements.append(members(i,1,self.n))

        