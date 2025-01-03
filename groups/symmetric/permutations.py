from tabulate import tabulate
from .symmetric import members as mm #
from itertools import permutations
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

        
        self.id = ...   #Take care of this 


        self.val = 0
        self._all = [str(i) for i in range(Noch)]
        self.elements = []
        self.group_order = Noch
        self._create_elements(Alt)
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

        if Alt == 1:
            print("In even")
            for i in temp:
                if even(i) == True:
                    self.elements.append(i)
        else:
            self.elements = temp

        for i in self.elements:
            i.inv = mm(self.group_order, i.inverse, )                   #Create instances by referencing to existing instance.    


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


    #--------------------------------------------------
    def adjacency(self
                  )->list:
        self.conjugacy_classes()
        l = [[0 for i in range(len(self.elements))] for j in range(len(self.elements))]
        keys = dict(zip([i.__str__() for i in self.elements], range(len(self.elements))))        
        # for cycles in self.classes:
        #     c = len(cycles)
        #     if c!= 1:
        #         for el in range(c):
        #             l[keys[cycles[el]]][keys[cycles[(el+1)%c]]] = 1
        #             l[keys[cycles[el]]][keys[cycles[(el-1)%c]]] = 1
        # for i in l:
        #     print(i)
        row = 0
        for i in self.elements:
            k = i
            for col in range(len(self.elements)):
                k = k*i
                if l[row][keys[k.__str__()]] == 0:
                    l[row][keys[k.__str__()]] = col
                col+=1
            row +=1
        
        self.cayleys()
        for i in l:
            print(i)
        return l
                    
    def __getitem__(self,
                    index):
        """
        Index the instance to get members.
        ---------------------------------
        input = index(int)
        return members[i]
        """
        return self.elements[index]
    
    def subgroups(self,
                  )->None:
        ...
    """
    Consider the subgroups generated by the non-generators, may have to find the cycles to find if it's a generator or not. 
    """     


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

    def edges_and_vertices(self
                           ):
        max_element, max_index = 0,0
        for i in self.elements:
            if i.order > len(i.cycles):
                max_element,max_index = i,len(i.cycles)
        vertices = circle(max_index)
        for el,pos in zip(i.cycles,vertices):
            el.position = pos
        


    def cosets(self,
               sub):
        """
        Given a subgroup find the cosets(let's start with right cosets)
        """
        

if __name__ == "__main__":
    k = Pgroup(3)
    for i in k.elements:
        print(i,str(i.inverse),type(i.inverse))