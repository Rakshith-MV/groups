from itertools import permutations
from math import factorial, lcm
from .group_base import Group, element
from .Decorators import _maptostr, _strtomap, class_cache, even
from .graphs import sphere
from functools import cache


class symmetric(Group):
    def __init__(self, 
                 order, 
                 Alt:bool,
                 generators:list = ['()']
                 )->None:
        super().__init__(order)
        self._all = [str(i) for i in range(order)]
        self._order = factorial(order) if Alt == 0 else factorial(order)//2
        self._elements = []
        self.create(Alt)
        self.maps = dict(zip([el._string for el in self._elements],range(self._order)))
        self.ord_inv()
        # self.update_graph(generators)
        self.edges = {}; self.vertices = []; self._generators = []
    def create(self,
               Alt):
        els = list(permutations(range(len(self._all))))
        if Alt == 1:
            for i in els:
                temp = members(len(self._all), element_d = dict(zip(self._all, [str(j) for j in i])))
                if even(temp) == 1:
                    self._elements.append(temp)
        else:
            for i in els:
                self._elements.append(members(len(self._all), element_d = dict(zip(self._all, [str(j) for j in i]))))   #This should probably be  len(self._all)

    def ord_inv(self):
        self._inverses = dict(zip(self._elements,[ 0 for i in self._elements]))
        for i in self._inverses:
            if self._inverses[i] == 0:
                temp  = self._elements[self.maps[_maptostr(len(self._all), dict(zip(i._dict.values(), i._dict.keys())))]]
                self._inverses[i] = temp
                self._inverses[temp] = i
                i._order = lcm(*[len(i) for i in i._string.split(',')])
                temp._order = i._order

    def update_graph(self,
                     generators:list = ['()']):
        """
        Update the graph representation of the symmetric group.
        """
        main_element = sorted(self._elements, key=lambda x: x._order)[-1]
        self.vertices = sphere(self._order, self._order//main_element._order)
        self._generators = []
        self.edges = dict(zip(range(self._order), [[] for _ in range(self._order)]))
        self._generators = generators
        for i in generators:
            for j in self._elements:
                self.edges[self.maps[j._string]].append(self.maps[j*i])
        

class members(element):
    def __init__(self,
                 gorder = int,
                 element_s:str=None,
                 element_d:dict=None
    )->None:
        self._all = [str(i) for i in range(gorder)] 
        self._gorder = gorder
        self.cycles = []
        self._dict   = element_d if element_d != None else _strtomap(len(self._all), element_s)
        self._string = element_s if element_s != None else _maptostr(len(self._all), element_d)

    def __mul__(self, other):
        new = {}
        for i in self._all:
            new[i] = self._dict[other._dict[i]]
        return members(self._gorder, element_d=new)

    def __str__(self) -> str:
        return '('+ self._string +')'
    

def test():
    s3 = symmetric(3, Alt=False)
    for i in s3:
        print(f" Order : {i._order}, Inverse : {s3._inverses[i]}, Element : {i._string}")
    print()
