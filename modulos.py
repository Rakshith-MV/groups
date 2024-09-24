from functools import cache, wraps
from Decorators import unitary
from tabulate import tabulate
import numpy as np


@cache
class members:
    """
    ======================================================================
    input : 
            element: and integer as a member of group
            n      : integer, number of elements in the group
            id     : identity element
            operation: lambda funtion ( to account for both * and + groups)
    ======================================================================
    """
    def __init__(self,
                 element: int,
                 n:int,
                 id:int,
                 operation  #lambda function
                ) -> None:
        self.group_order = n
        self.id = id
        self.element = element
        self.op = operation
        self.order_cycles()

    def order_cycles(self
                     )->None:
        k  = self.element
        count = 1
        self.string = ""
        self.order = 1

        while(str(self.element) not in self.string ):
            if self.element == 0:
                print(self.string)
            inverse = k
            if k == self.id:
                self.order = count
                self.inverse = inverse
            
            k = self.op(k,self.element,self.group_order)
            self.string += str(k)
            count+=1
        self.string = self.string[-1]+self.string[:-1]

    def __pow__(self,
                n:int
                )->int:
        temp = self.id
        for i in range(n):
            temp = self.op(temp,self.element,self.group_order)
        return temp

    def __int__(self
                )->int:
        return self.element
    
    def __add__(self,
                i
                ):  
        return (self.element+i.element)%self.group_order
    
    def __mul__(self,
                i:int
                ):
        return members((self.element*i)%self.group_order,self.group_order,self.id, self.op)

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
        if operation == "*":
            self.id = 1
            self.op = lambda a,b,n : (a*b)%n
            self.elements= [members(i,n,self.id,self.op) for i in unitary(n)]
        else:
            self.id = 0
            self.op = lambda a,b,n : (a+b)%n
            self.elements = [members(i,n,self.id,self.op) for i in range(n)]
        self.noch = n

    def cayleys(self
                )->None:
        if self.id == 0:
            table = [[ int(i) for i in self._cycles(e)] for e in range(len(self.elements))]
            self.matrix = np.matrix(table)
            print(tabulate([[str(i)+"  ", *table[i]] for i in range(len(self.elements))],["# ",*list(range(len(self.elements)))],"grid"))
        else:
            table = [[ i.__str__() for i in self._cycles(int(e))] for e in  self.elements]
            print(tabulate([[str(i)+"  ", *table[i]] for i in self.elements],["# ",*self.elements],"grid"))

    def subgroups(self,    
                  )->set:
        self.subgroups = set()
        
        #CYCLIC SUBGROUPS
        #=========================
        for i in self.elements:
            self.subgroups.add(self._cycles(i))
        
        #USING MULTIPLE ElEMENTS AS GENERATORS
        # =======================================
        


        # CENTER OF A GROUP, CENTROID OF A GROUP, 


        # 
    def generators(self
                   ):
        if self.id == 0:
            return [i.element for i in self.elements if len(i.string) == self.noch]
        return [ i.element for i in self.elements]

    @cache
    def _cycles(self,
                i:int
                )->set:

        if self.id == 0:
            temp = [self.elements[e+self.elements[i]] for e in self.elements]
            return temp
        else:
            temp = [e*i for e in self.elements]
            return temp
        
    def __sizeof__(self) -> int:
        self.noch

    def __getitem__(self,
                    n:int):
        return self.elements[n]
    
    def __str__(self) -> str:
        s = "Elements : "
        for i in self.elements:
            s+=str(i.element)+', '
        return s.rstrip(',')
    

