from ..modulo import modulos
from ..symmetric import permutations

from ..dihedral.Dihedral import Dn
from functools import cache, wraps
from math import prod
from tabulate import tabulate

class members:
    def __init__(self,
                 a:tuple,
                 id:tuple,
                 nogs :int
                 )-> None:
        self.element = a
        self.id = id 
        self.nogs = nogs

    def __mul__(self,
                a:any
                )->any:
        try:          #IF nogs is not necessary in the future remove it by replacing the range8(len(a))
            return members([a[i]*self.element[i] for i,j in zip(range(self.nogs),range(self.nogs))],self.id, self.nogs)     
        except:
            return members([a.element[i]*self.element[j] for i,j in zip(range(self.nogs),range(self.nogs))],self.id, self.nogs)

    def at(self
           )-> str:
        return tuple([str(i) for i in self.element])
    def __str__(self
                ) -> str:
        return str(tuple([str(i) for i in self.element]))

class Gprod(members):
    """
    ==========================================================
    input:
        List of groups as a list
    """
    def __init__(self,
                 groups:list
                 ):
        self.noch = 1; self.id = []; 
        self.elements = [[i] for i in groups[0].elements]
        self.nogs = len(groups)
        for i in groups:
            self.noch *= i.group_order
            self.id.append(i.id)
        self.id = tuple(self.id)
        temp  = []
        for g in groups[1:]:
            temp1 = []
            for elem in self.elements:
                temp2 = []
                for newe in g.elements:
                    temp2.append(elem+[newe])
                temp1 += temp2
            self.elements = temp1
        self.elements = [members(i,self.id,self.nogs) for i in self.elements]

    def __str__(self) -> str:
        s = ""
        for i in self.elements:
            s+="("
            for j in i.element:
                s+=str(j)+','
            s = s.rstrip(',')
            s += ')'+'\n'
        return s
                

    def _cycles(self,
                e)->any:
        return [e*i for i in self.elements]


    def cayleys(self
                ):
        table = [[ i.__str__() for i in self._cycles(e)] for e in  self.elements]        
        print(tabulate([[str(self.elements[i])+"  ", *table[i]] for i in range(len(self.elements))],["# ",*self.elements],"grid"))
        


if __name__ == "__main__":
    k = Gprod([modulos(3),modulos(2)])
    print(k)
    k.cayleys()