from itertools import permutations
from math import factorial
from sympy import N
from .group_base import Group, element
from .Decorators import _maptostr, _strtomap, class_cache
from functools import cache


class symmetric(Group):
    def __init__(self, 
                 order, 
                 Alt:bool,
                 generators:list = None
                 )->None:
        super().__init__(order)
        self._all = [str(i) for i in range(order)]
        self._order = factorial(order) if Alt == 0 else factorial(order//2)
        self.elements = []
        self.create(Alt)
        self.maps = dict(zip([el.string for el in self.elements],range(self.number_of_elements)))
        self.edges = ...
        

        self.update_graph(generators)


    def create(self,
               Alt):
        els = list(permutations(range(self._order)))
        if Alt == 1:
            for i in els:
                temp = members(self._order, element_d = dict(zip(self._all, [str(j) for j in i])))
                if even(temp) == 1:
                    self.elements.append(temp)
        else:
            for i in els:
                self.elements.append(members(self._order, element_d = dict(zip(self._all, [str(j) for j in i]))))

    def cygroup(self):
        ...
        


class members(element):
    def __init__(self,
                 gorder = int,
                 element_s:str=None,
                 element_d:dict=None,
                 inverse:object=None
    )->None:
        self._all = [str(i) for i in range(gorder)]
        self.color = "white" 
        self._gorder = gorder
        # # self.cycles = []
        # self._maps = element_d if element_d != None else _strtomap(gorder, element_s)
        # self._string = element_s if element_s != None else _maptostr(gorder, element_d)
        # self.inverse = members(group_order, element_d = dict(zip(self.maps.values(), self.maps.
