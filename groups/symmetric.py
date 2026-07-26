from itertools import permutations
from math import factorial, lcm
from .group_base import Group, element
from .Decorators import _maptostr, _strtomap, class_cache, even
from .graphs import cylinder, sphere
from functools import cache

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
        self._identity = self._elements[0]
        
        self._maps = dict(zip([i._string for i in self._elements], self._elements))
        self._gmaps = dict(zip(self._elements, range(self._order)))
        self.ord_inv()
        self.update_graph(generators)

    def create(self, Alt):
        els = list(permutations(range(len(self._all))))
        if Alt == 1:
            for i in els:
                temp = members(len(self._all), self, element_d = dict(zip(self._all, [str(j) for j in i])))
                if even(temp) == 1:
                    self._elements.append(temp)
        else:
            for i in els:
                self._elements.append(members(len(self._all), self, element_d = dict(zip(self._all, [str(j) for j in i]))))

    def ord_inv(self):
        self._inverses = dict(zip(self._elements, [0 for i in self._elements]))
        for i in self._inverses:
            if self._inverses[i] == 0:
                temp = self._maps[_maptostr(self.n, dict(zip(i._dict.values(), i._dict.keys())))]
                self._inverses[i] = temp
                self._inverses[temp] = i
                i._order = lcm(*[len(x) for x in i._string.split(',') if x])
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
        
        is_alt = (self._order == factorial(self.n) // 2) if self.n >= 2 else False

        if not generators or generators == ['()'] or generators == ['']:
            generators = []
            identity_str = ','.join(str(k) for k in range(self.n))
            if not is_alt:
                trans = None
                cycle = None
                for el in self._elements:
                    fixed_count = sum(1 for k, v in el._dict.items() if k == v)
                    if fixed_count == self.n - 2:
                        trans = el._string
                    elif fixed_count == 0:
                        cycle = el._string
                if trans:
                    generators.append(trans)
                if cycle:
                    generators.append(cycle)
            else:
                count = 0
                for el in self._elements:
                    fixed_count = sum(1 for k, v in el._dict.items() if k == v)
                    if fixed_count == self.n - 3:
                        generators.append(el._string)
                        count += 1
                        if count >= 2:
                            break
            if not generators:
                non_id = [el._string for el in self._elements if el._string != identity_str]
                if non_id:
                    generators = [non_id[0]]

        self._generators = generators
        self.edges = dict(zip(range(self._order), [[] for _ in range(self._order)]))
        
        for gen_item in generators:
            if isinstance(gen_item, members):
                el = gen_item
            else:
                gen_str = str(gen_item).strip()
                stripped = gen_str.strip('()')
                el = self._maps.get(stripped) or self._maps.get(gen_str)
            if el is not None:
                for j in self._elements:
                    target_el = j * el
                    self.edges[self._gmaps[j]].append(self._gmaps[target_el])


class members(element):
    def __init__(self,
                 gorder = int,
                 group=None,
                 element_s:str=None,
                 element_d:dict=None
    )->None:
        super().__init__()
        self._all = [str(i) for i in range(gorder)] 
        self._gorder = gorder
        self.cycles = []
        self._dict = element_d if element_d != None else _strtomap(len(self._all), element_s)
        self._string = element_s if element_s != None else _maptostr(len(self._all), element_d)
        self._group = group

    def __mul__(self, other):
        new = {}
        for i in self._all:
            new[i] = self._dict[other._dict[i]]
        return self._group._maps[_maptostr(len(self._all), new)]

    def __str__(self) -> str:
        return '('+ self._string +')'