"""
At somepoint the software should take abstract arbitrary set and see if if forms a group. 
The real question answered by cayley was can an abstract group created properly represent 
an usefull symmetry of some object. 

Can that object be pointed out??? some sources says *Hell yeah*, haven't found anything usefull as of now, 
better question is what is the smallest symmetric group which contains a homomorphic copy of the given group. 

Ofcourse if the group is cyclic then.
1===> take an n permutation in a group of order >= n.


"""



from functools import cache
import math as mt

from .Decorators import powerset, prime_decomposition
from .graphs import circle
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
    Required attributes:
            order, inverse. 
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

    def __matmul__(self,
                     i:int):
        """
        This is defined for operation between a group element and an integer(modulo).
        """
        if self.op == '*':  
            return members((self.element*i)%self.group_order,
                           self.group_order,self.id, self.op) 
        return members((self.element+i)%self.group_order,
                       self.group_order,self.id, self.op)
        
    def __mul__(self,
                i:any
               ):
        """
        Defined for the operation between group elements.
        """
        try:
            if self.op == '*':
                return members((self.element*i)%self.group_order,
                               self.group_order,self.id, self.op)
            return members((self.element+i)%self.group_order,
                           self.group_order,self.id, self.op)
        except TypeError:
            if self.op == '*':
                return members((self.element*i.element)%self.group_order,
                               self.group_order,self.id, self.op)
            return members((self.element+i.element)%self.group_order,
                           self.group_order,self.id, self.op)

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

# @cache
class modulo:
    """
    A modulo group of order n, with operation + or *.
    =========================================

    input : n-> integer
            operation -> character
    
    ouput: object with indexing available to access elements.

    ------------------------------------------------------------
    print(object) to find elements with indexes.
    -----------------------------------------------------------
    Required attributes(isomorphism):
            elements, group_order.  
    ------------------------------------------------------------
    """
    def __init__(self,
                 n:int,
                 operation:chr="+",
                 generator:int=[]
             121 ) -> None:
        self.op = operation
        if operation == "*":
            self.id = 1
            self.elements= [members(i,n,self.id,operation) 
                            for i in range(n) 
                            if mt.gcd(i,n) == 1]
            self.group_order = len(self.elements)
            self.maps = dict(zip(self.elements,range(self.group_order)))
        else:
            self.id = 0
            self.group_order = n    
            self.elements = [members(i,n,self.id,operation) 
                             for i in range(n)]
            self.maps = dict(zip(self.elements,range(self.group_order)))
        self.find_generators()
        for i,j in zip(self.maps.keys(), self.maps.values()):
            if j == generator:
                self.gen = i
                break
        self.edges_and_vertices(generator)
        #There is a probability that the element might not be in the set. for now it's working let's see.


    def inverses(self
                )->None:
        """
        Find inverses of the elements
        """
        for i in self.elements:
            # i.order  = len(self.elements)
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
        """
        Table
        """
        return [[ i for i in self._cycles(e.element)] 
                for e in  self.elements]

    def find_generators(self
                   ):
        self.inverses()
        if self.op == '*':
            self.gen = self.elements
            return
        self.gen =  [i for i in self.elements if i.order == len(self.elements)]
    
    def subgroups(
            self
            )->tuple:
        factors, possible_subgroups = prime_decomposition(self.group_order)
        index = max(factors.values())
        print(factors,index)
        for i in factors.keys():
            if factors[i] == index:
                main = i**index
                break
        # for i in self.elements:
        #     if i.order == main:
        #         gen = i
        #         break
        # cycles = [self._cycles(i)]
        # return cycles


    @cache
    def _cycles(self,
                i:int
                )->set:
        """
        all the resulting elements by operating from a particular element.
        """
        return [e*i for e in self.elements]

    def edges_and_vertices(self,
                           generator=[]
                            ):
        if generator == []:
            generator = [str(self.maps[random.choice(self.elements[1:])])]
        self.generators = generator
        self.edges = {}
        for i in self.elements:
            self.edges[self.maps[i]] = [self.maps[i@int(j)] for j in self.generators]
        self.vertices = circle(self.group_order)

    def __len__(self) -> int:
        return len(self.elements)

    def __getitem__(self,
                    n:int):
        return self.elements[n]
    
    def __str__(self) -> str:
        return [i.__str__() for i in self.elements]
        
if __name__ == "__main__":
    k = modulo(10,'+')
    k.edges_and_vertices()

