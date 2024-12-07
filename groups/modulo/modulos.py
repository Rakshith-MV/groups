"""
At somepoint the software should take abstract arbitrary set and see if if forms a group. 
The real question answered by cayley was can an abstract group created properly represent 
an usefull symmetry of some object. 

Can that object be pointed out??? some sources says *Hell yeah*, haven't found anything usefull as of now, 
better question is what is the smallest symmetric which is homomorphic to the given group. 

Ofcourse if the group is cyclic then.
1===> take an n permutation in a group of order >= n.


"""



from functools import cache
# from tabulate import tabulate
import math as mt
from ..helpers.Decorators import powerset
from ..helpers.graphs import circle
import random

@cache
class members:
    """
    ======================================================================
    input : 
            element: and integer as a member of group
            n      : integer, number of elements in the group
            id     : identity element
            operation: character 
    ======================================================================
    """
    def __init__(self,
                 element: int,
                 n:int,
                 id:int,
                 operation:chr
                ) -> None:
        self.color = 'white'
        self.group_order = n
        self.id = id
        self.element = element
        self.op = operation
        self.order = 0; self.inverse = id

    def __mul__(self,
                i:any
               ):
        try:
            if self.op == '*':
                return members((self.element*i)%self.group_order,self.group_order,self.id, self.op)
            return members((self.element+i)%self.group_order,self.group_order,self.id, self.op)
        except TypeError:
            if self.op == '*':
                return members((self.element*i.element)%self.group_order,self.group_order,self.id, self.op)
            return members((self.element+i.element)%self.group_order,self.group_order,self.id, self.op)
        
    def __pow__(self,
                n:int
                )->int:
        temp = self.id
        for i in range(n):
            temp = self.element*temp   #self.op(temp,self.element,self.group_order)  Trying to remove the self.op operator
        return temp

    def __int__(self
                )->int:
        return self.element

    def __str__(self) -> str:
        return str(self.element)

@cache
class modulo:
    """
    A modulo group of order n, with operation + or *.
    =========================================

    input : n-> integer
            operation -> character
    
    ouput: object with indexing available to access elements.

    ------------------------------------------------------------
    print(object) to find elements with indexes.
    ------------------------------------------------------------
    """
    def __init__(self,
                 n:int,
                 operation:chr="+",
                 ) -> None:
        self.group_order = n
        self.op = operation
        if operation == "*":
            self.id = 1
            self.elements= [members(i,n,self.id,operation) 
                            for i in range(n) 
                            if mt.gcd(i,n) == 1]
        else:
            self.id = 0
            self.elements = [members(i,n,self.id,operation) 
                             for i in range(n)]
        self.find_generators()
        self.edges_and_vertices()      #Creates edges and vertices, may be unnecessary if looking only for table, but small groups should be fine. 

    def inverses(self
                )->None:
        for i in self.elements:
            i.order  = len(self.elements)
            k = 1
            temp = i
            i.inverse = temp
            while (temp.element != self.id):
                i.inverse = temp
                temp*=i
                k+=1
            i.order = k

    def cayleys(self
                )->None:
        table = [[ i for i in self._cycles(e.element)] for e in  self.elements]
        #print(tabulate([[str(self.elements[i])+"  ", *table[i]] for i in range(len(self.elements))],["# ",*self.elements],"grid"))
        return table

    def find_generators(self
                   ):
        self.inverses()
        self.generators =  [i for i in self.elements if i.order == len(self.elements)]
    
    def subgroups(
            self
            )->tuple:
        ...

    @cache
    def _cycles(self,
                i:int
                )->set:
        temp = [e*i for e in self.elements]
        return temp
        
    
    def edges_and_vertices(self,
                           ):
        i = random.choice(self.generators)
        cycles = self._cycles(i)
        self.edges = {}
        self.vertices = circle(self.group_order)
        for j in range(len(cycles[:-1])):
            self.edges[int(str(cycles[j]))] = [int(str(cycles[j+1]))]
        self.edges[int(str(cycles[-1]))] = [int(str(cycles[0]))]


    def __len__(self) -> int:
        return len(self.elements)

    def __getitem__(self,
                    n:int):
        return self.elements[n]
    
    def __str__(self) -> str:
        s = "Elements : "
        for i in self.elements:
            s+=str(i.element)+', '
        return s.rstrip(',')
    
        
if __name__ == "__main__":
    k = modulo(10,'+')
    k.edges_and_vertices()

