"""
Permutation groups as the name says.
Gives all the permutations of a string(n : int).
"""
from functools import cache
from math import factorial
import sys
import os
from itertools import permutations

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from os import name
from helpers.Decorators import custom_cache, class_cache, _maptostr,_strtomap, even
from math import lcm
from helpers.graphs import sphere

@class_cache
class members:
    def __init__(self,
                 group_order:int,
                 element_s:str=None,
                 element_d:dict=None,
                 inverse:object=None    
                ) -> None:
        self._all = [str(i) for i in range(group_order)]
        self.color = "white"
        self.group_order = group_order        
        self.cycles = []
        self.maps = element_d if element_d != None else _strtomap(group_order,element_s)
        self.string = element_s if element_s != None else _maptostr(group_order,element_d)  #there must be ',' in between small cycles
        self.inverse = members(group_order,element_d=dict(zip(self.maps.values(), self.maps.keys())),inverse=self) if inverse == None else inverse
        self.order = lcm(*[len(i) for i in self.string.split(',')])   #Do i need and exceptions????
        if self.order == 0:
            self.order = 1 

    def __mul__(self, 
                sec:object
                 )->object:
        new = {}
        for i in self._all:
            new[i] = self.maps[sec.maps[i]]
        return members(self.group_order, element_d=new)



    
    def __str__(self):
        return '('+ self.string +')'
    
        




class Sn:
    def __init__(self,
            group_order,
            Alt:bool=0,
            generators:list=None
            )->None:
        self._all = [str(i) for i in range(group_order)]
        self._id = dict(zip(self._all,self._all))
        self.group_order =group_order
        self.number_of_elements = factorial(group_order) if Alt == 0 else int(factorial(group_order)/2)
        self.elements = []
        self.create(Alt)
        self.maps = dict(zip([el.string for el in self.elements],range(self.number_of_elements)))
        self.edges = dict(zip([self.maps[el.string] for el in self.elements],[[] for i in range(self.number_of_elements)]))
        # print(generators)
        self.cygroup()
        self.edges_and_vertices(generators)


    def create(self,
               Alt
               )->None:
        els = list(permutations(range(self.group_order)))
        if Alt == 1:
            for i in els:
                temp = members(self.group_order, element_d=dict(zip(self._all,[str(j) for j in i])))
                if even(temp) == 1:
                    self.elements.append(temp)
        else:
            for i in els:
                self.elements.append(members(self.group_order, element_d=dict(zip(self._all,[str(j) for j in i]))))


    def cayleys(self
                ):
        return [[i*j for i in self.elements] for j in self.elements]

    # It appears to be much easier to find cycles in the main group.!!!
    def cygroup(self):
        for element in self.elements:
            element.cycles=  [element]
            for i in range(element.order-1):
                element.cycles.append(element.cycles[-1]*element)

    def edges_and_vertices(self,
                           gen:list=None):
        """"
        Order based on the main cycle selected!!!
        How do you remove duplicate cosets??,
        """
        #select the element for the main cycle
        main_element = self.elements[0]
        for i in self.elements:
            if main_element.order < i.order:
                main_element = i
        ordered_elements = main_element.cycles
        selected_elements = [self.maps[i.string] for i in ordered_elements]
        for i in self.elements:
            if self.maps[i.string] not in selected_elements:
                temp = [k*i for k in main_element.cycles]
                for t in temp:
                    ordered_elements.append(t)
                    selected_elements.append(self.maps[t.string])
        self.vertices = sphere(main_element.order,int(self.number_of_elements/main_element.order))
        self.names = [i.string for i in ordered_elements]
        self.generators = [main_element.string] if gen == [] or gen ==None else gen
        for j in self.generators:
            el = self.elements[self.maps[j]]
            for i in self.elements:
                self.edges[self.maps[i.string]].append(self.maps[(i*el).string])

    def __getitem__(self,
                    i):
        return self.elements[i]
        

if __name__ == "__main__":
    k = Sn(3,1)