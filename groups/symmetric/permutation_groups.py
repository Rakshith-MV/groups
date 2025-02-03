import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from os import name
from helpers.Decorators import custom_cache, class_cache, _maptostr,_strtomap
from math import lcm

class members:
    def __init__(self,
                 group_order:int,
                 element_s:str=None,
                 element_d:dict=None,
                 inverse:object=None
                ) -> None:
        self.color = "white"
        self.group_order = group_order        
        self.cycles = []
        self.maps = element_d if element_d != None else _strtomap(group_order,element_s)
        self.string = element_s if element_s != None else _maptostr(group_order,element_s)  #there must be ',' in between small cycles
        self.inverse = members(group_order,element_d=dict(zip(self.maps.values(), self.maps.keys())),inverse=self) if inverse == None else inverse
        self.order = lcm([len(i) for i in self.string.split(',')])


    
    
        




class permutation(members):
    def __init__(self,
            group_order
            )->None:
        
        self._all = [str(i) for i in range(group_order)]
        self._id = dict(zip(self._all,self._all))
        self.group_order = group_order

    #much easier to create if the elements have already been created!!
    def cygroup(self,
                element):
        self.cycles=  [self]
        for i in range(self.order-1):
            self.cycles.append(self.cycles[-1]*self)




if __name__ == "__main__":
    k = permutation(4)
