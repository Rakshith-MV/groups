from itertools import permutations
from math import factorial, lcm
from .group_base import Group, element
from .Decorators import _maptostr, _strtomap, class_cache, even
from .graphs import cylinder, sphere
from functools import cache


maps = {}
gmaps = {}
class symmetric(Group):
    def __init__(self, 
                 order, 
                 Alt:bool,
                 generators:list = ['()']
                 )->None:
        self.n = order
        super().__init__(order)
        self._all = [str(i) for i in range(order)]
        self._order = factorial(order) if Alt == 0 else factorial(order)//2
        self._elements = []
        self.create(Alt)
        global maps, gmaps
        maps = dict(zip([i._string for i in self._elements],self._elements))
        gmaps = dict(zip(self._elements, range(self._order)))
        self.ord_inv()
        self.update_graph(generators)
        # self.edges = {}; self.vertices = []; self._generators = []

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
                temp  = maps[_maptostr(self.n,dict(zip(i._dict.keys(),i._dict.values())))]
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
        print(f"order : {self._order}\n main element : {main_element}, {main_element._order}")
        self.vertices = cylinder(main_element._order, self._order//main_element._order)
        print(f"Vertinces {self.vertices}, {len(self.vertices)}")
        self._generators = []
        self.edges = dict(zip(range(self._order), [[] for _ in range(self._order)]))
        self._generators = generators
        for i in generators:
            el = maps[i]
            for j in self._elements:
                self.edges[gmaps[maps[j._string]]].append(gmaps[j*el])
        print(self._generators) 
        print(self.edges)


    def __hash__(self):
        return hash(self._elements)



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
        return maps[_maptostr(len(self._all),new)]

    def __str__(self) -> str:
        return '('+ self._string +')'