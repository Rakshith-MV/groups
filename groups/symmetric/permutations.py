from ast import main
from enum import member
from .symmetric import members as mm #
from itertools import cycle, permutations
from functools import cache
from ..helpers.Decorators import even    #
from ..helpers.graphs import circle

val = 0
              
#Reduced number of times the same instance created, not sure if it affects somehow, the program
#It shoudn't as there won't be any change in objects
@cache
class Pgroup():
    """
    Takes an input integer, forms a corresponding permutation group, with a range of integers.
    input : integer
    ____________________________
    n = 3
    creates, members of elements:
    012, 021, 12, 02, 01, .
    ____________________________

    Inverses are auto initialized.
    run conjugacy_classes to form, equivalence conjugacy classes -> self.classes

    A class method to find conjugate elements of an element (Conjugate_elements).

    print(instance) -> returns index and it's element as a string.
    
    """
    def __init__(self, 
                 Noch : int,
                 Alt :bool = 0):      #Noch number of characters

        
        self.max = 0
        self.id = ...   #Take care of this 
        self.val = 0
        self._all = [str(i) for i in range(Noch)]
        self.elements = []
        self.group_order = Noch
        self._create_elements(Alt)
        self.indexes = dict(zip([i.string for i in self.elements], self.elements))
        global val
        val +=1
        
    
    def _create_elements(self,
                         Alt: bool
                     )->None:
        els = list(permutations(range(self.group_order)))
        temp = []
        for i in els:
            temp.append(mm(self.group_order, dict(zip(self._all,[str(j) for j in i]))))
            self.val += 1
            self.max = max(temp[-1].order,self.max)

        if Alt == 1:
            for i in temp:
                if even(i) == True:
                    self.elements.append(i)
        else:
            self.elements = temp

        for i in self.elements:
            i.inv = mm(self.group_order, i.inverse, )                   #Create instances by referencing to existing instance.    

    #Don't know if this is necessary, but it's a good idea to have it.
    def clear_coset_data(self,
                        i:object = None): 
        for j in i:
            j.coset_index  = 1
        if i == None:
            for j in self.elements:
                j.coset_index = 0

    def cosets_of_cycles(self,
                         i):
        k = set()
        sub = [self.mapi.cycles]
        k.add(sub)
        self.clear_coset_data(k[-1])
        for j in self.elements:
            if j.coset_index == 0:
                k.add([j*i for i in sub])
                self.clear_coset_data(k[-1])
    

    def compute_conjugacy_classes(self
                          )->list:
        """
        sets of conjugate elements, which form self conjugate sets, 
        Every element belongs to a unique class.
        
        _conjugate_elements : creates a set of conjugate elements for a given element.
        __________________________________
        could use @cache to reduce time, but using the set unions to find if it's already been in a class 
        makes it faster.
        __________________________________
        "Can Randomization increase speed??"
        """
        self.conjugacy_classes = []
        elements_used = set()
        for i in self.elements:
            if str(i) not in elements_used:
                c = self._conjugate_elements(i)
                self.conjugacy_classes.append(list(c))
                elements_used = elements_used | c
            if len(elements_used) == self.group_order:
                break
        return self.conjugacy_classes
        
    
    def _conjugate_elements(self,
                          a:object
                          )->list:
        """
        Helper function to conjugacy_classes.
        """
        l = set()
        for i in self.elements:
            k = (i*a*i.inv).__str__()
            if k not in l:
                l.add(k)
        return l
    
    def coset(subs:list,
              el:member):
        temp = []
        for i in subs:
            temp.append(i*el)

    def main_cycle_and_cosets(self):
        """
        Find the main cycle and the cosets of the main cycle.
        """
        for i in self.elements:
            if i.order == self.max:
                main_element = i
                break
        cycles = set(main_element.cycles)
        count = len(cycles[-1])
        k = iter(self.elements)
        while count<self.group_order:
            self.coset(cycles[0],k.__next__())


    def edges_and_vertices(self,
                            generators
                            ):
        """
        The idea here would be to arrange the elements in such a way that, the main subgroup is generated to form the main cycle.
        rest of the elements forms the cosets of these elements.
        """
        #Assume just one generators per selection.
        #we can bring subgroups to picture as well
        main_cycle = generators.cyc
        

    def __getitem__(self,
                    index):
        """
        Index the instance to get members.
        ---------------------------------
        input = index(int)
        return members[i]
        """
        return self.elements[index]
    
    
    def cayleys(self
                )->None:
        table = []
        # print("------"*len(self.elements))
        for i in self.elements:
            temp = []
            for j in self.elements:
                temp.append(i*j)
                # print(i*j,end="   ")
            # print("\n","------"*len(self.elements))
            table.append(temp)
        return table

    def __str__(self
                )-> str:
        """
        Prints out elements with their indexes, class instance with indexing gives
        respective elements.
        """
        s = ""
        k = 0
        for i in self.elements:
            s+= str(k)+ " --> "+i.__str__()+'\n'
            k+=1
        return s

if __name__ == "__main__":
    k = Pgroup(2)
    for i in k.elements:
        print(i.cycles())