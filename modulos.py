from functools import cache, wraps
from Decorators import unitary


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
        temp =  k  = self.element
        count = 1
        self.string = ""
        self.order = 1
        if k == 0:
            return

        while(str(k) not in self.string):
            if k == id:
                self.order = count
                self.inverse = temp
            self.string += str(k)
            temp = k
            k = self.op(k,self.element,self.group_order)
            count+=1

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
                 operation:chr,
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
        print( "  | " , end= '')
        for i in self.elements:
            print(i.element , end="  |  " )
        print('\n',len(self.elements)*'------')    
        for i in self.elements:
            print(i.element,end =" | ")
            for j in self.elements:
                print(self.op(int(i.element),int(j.element),self.noch),end="  |  ")
            print()

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

    @cache
    def _cycles(self,
                i
                )->set:
        temp = ()
        for e in self.elements:
            temp.add(self.op(i,e))
        return temp

    def __getitem__(self,
                    n:int):
        return self.elements[n]
    
    def __str__(self) -> str:
        s = "Elements : "
        for i in self.elements:
            s+=str(i.element)+', '
        return s.rstrip(',')

if __name__ == "__main__":
    a = modulo(69,"+")
