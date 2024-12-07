"""
permutative elements, for a ring(literally not mathematically)
All members are taken to the right side, as in, if a*b then it's a[b[i]]
"""
from functools import cache, wraps
from ..helpers.Decorators import custom_cache, class_cache, _maptostr  
# from .colors import choose

@class_cache
class members:
    "  doc strings "
    def __init__(self,
                group_order: int,
                element_s:str = None,
                element_m :dict = None,
                ):
        self.color = 'white'
        self.noch = group_order                                                    #noch == number of characters
        self._all = [str(i) for i in range(group_order)]                           #list of characters
        self._id = dict(zip(self._all, self._all))                                 #Identity
        self.cycles = []
        self.maps = element_m
        self.string = element_s
        self.inverse : object
        self.cygroup()                                                          


    @custom_cache
    def __mul__(self, 
                sec:object
                 )->object:
        new = {}
        for i in self._all:
            new[i] = self.maps[sec.maps[i]]
        return members(self.noch, new)

    @custom_cache
    def __rmul__(self,
                 sec:object
                    )->object:
        new = {}
        for i in sec._all:
            new[i] = sec.maps[self.maps[i]]
        return members(self.noch, new)

    def __matmul__(self,
                   sec:dict
                     )->dict:
        new = {}
        for i in self._all:
            new[i] = self.maps[sec[i]]
        return new
    
    def __eq__(self, value: object) -> bool:
        if self.maps != self.maps:
            return False
        return True

    def cygroup(self
               ):
        """
        Computes order, inverse and the cycle( as in powers)
        of elements it produces, (finite groups only)
        """
        prod = self.maps
        n = 1
        temp = prod
        while(prod not in self.cycles):   
            if prod == self._id:
                self.order = n
                self.inverse = _maptostr(self.noch, temp)
            self.cycles.append(prod)
            n+=1
            temp = prod
            prod = self@prod

    def transpositions(self
                       )->bool:
        """
        There are many possible ways to write a transposition\n
        possibly infinite, there is just one possible implementation here, 
        if required write some more stuff and use a random number generator
        """
        self.trans = []
        for i in self.string[:-1]:
            self.trans.append(self.string[-1]+i)
        print(self.trans)
        if len(self.trans)%2 == 0:
            return True
        return False

    def info(self
             ):
        self.transpositions()
        return [self.__str__(),self.order,_maptostr(self.noch,self.inverse),[_maptostr(self.noch,i) for i in self.cycles],self.trans]

    def __str__(self
                ) -> str:
        s = ""
        for i in self.string.split(','):
            s+='('+i+')'
        return s                      
    
    
if __name__ == "__main__":
    ...      