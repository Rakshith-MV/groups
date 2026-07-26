import math
from functools import reduce
from .group_base import Group, element
from .graphs import circle

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

class ProductElement(element):
    def __init__(self, components, group):
        super().__init__()
        self.components = tuple(components)
        self._group = group
        self._string = f"({','.join(str(c) for c in self.components)})"
        # order is lcm of order of components
        self._order = reduce(lcm, [c._order for c in self.components], 1)

    def __mul__(self, other):
        if not isinstance(other, ProductElement):
            # Allow multiplication with elements representing component elements
            # (fallback to other if other is not element but it has elements)
            return super().__mul__(other)
        
        prod_components = []
        for a, b in zip(self.components, other.components):
            prod_components.append(a * b)
        
        target_str = f"({','.join(str(c) for c in prod_components)})"
        res = self._group._element_by_str.get(target_str)
        if res is not None:
            return res
        return ProductElement(prod_components, self._group)

    def __eq__(self, other):
        if isinstance(other, ProductElement):
            return self.components == other.components
        return False

    def __hash__(self):
        return hash(self.components)

    def __str__(self):
        return self._string


class ProductGroup(Group):
    def __init__(self, groups_list, generators=None):
        self.subgroups_list = groups_list
        
        order = 1
        for g in groups_list:
            order *= len(g._elements)
        super().__init__(order)
        self._order = order

        import itertools
        self._elements = []
        self._element_by_str = {}
        
        subgroups_elements = [g._elements for g in groups_list]
        for combo in itertools.product(*subgroups_elements):
            el = ProductElement(combo, self)
            self._elements.append(el)
            self._element_by_str[str(el)] = el

        # Identity
        self._identity = self._element_by_str[f"({','.join(str(g._identity) for g in groups_list)})"]

        # Inverses
        self._inverses = {}
        for el in self._elements:
            inv_components = []
            for i, c in enumerate(el.components):
                g = self.subgroups_list[i]
                inv_components.append(g._inverses[c])
            inv_str = f"({','.join(str(inv_c) for inv_c in inv_components)})"
            self._inverses[el] = self._element_by_str[inv_str]

        # Generator selection
        if not generators:
            generators = []
            for i, g in enumerate(self.subgroups_list):
                sub_gens = getattr(g, '_generators', [])
                if not sub_gens or callable(sub_gens):
                    sub_gens = getattr(g, 'generators', [])
                if callable(sub_gens):
                    sub_gens = []
                
                sub_gens_str = [str(x) for x in sub_gens]
                if not sub_gens_str:
                    non_id = [str(x) for x in g._elements if x != g._identity]
                    if non_id:
                        sub_gens_str = [non_id[0]]
                for sg in sub_gens_str:
                    comp = []
                    for j, other_g in enumerate(self.subgroups_list):
                        if i == j:
                            comp.append(sg)
                        else:
                            comp.append(str(other_g._identity))
                    generators.append(f"({','.join(comp)})")
        
        self.generators = generators
        self._generators = [self._element_by_str[g] for g in generators if g in self._element_by_str]
        self.update_graph(generators=generators)

    def update_graph(self, generators):
        self.generators = generators
        self.edges = {}
        
        el_to_index = {str(el): idx for idx, el in enumerate(self._elements)}
        
        for idx, el in enumerate(self._elements):
            targets = []
            for gen_str in self.generators:
                gen_el = self._element_by_str.get(gen_str)
                if gen_el:
                    prod = el * gen_el
                    targets.append(el_to_index[str(prod)])
            self.edges[idx] = targets

        self.vertices = circle(self._order)
