class element:
    def __init__(self
                 )->None:
        self.order = None

    def __mul__(self,
                other
                ):
        raise NotImplementedError
    
    def __matmul__(self,
                 other
                 ):
        raise NotImplementedError

    def __pow__(self,
                n):
        temp = self
        for i in range(n-1):
            temp*= self
        return temp

    def __int__(self):
        return self._number
    
    def __str__(self):
        return str(self._number)


class Group:
    def __init__(self,
                 order,
                 **kwargs) -> None:
        self._identity = None
    
    def elements(self
                 ):
        return self._elements
    
    def cayleys(self
               ):
        return [[i*j for j in self._elements] for i in self._elements]
     
    def generators(self
                    ):
        self.generators = [i for i in self._elements if i.order == self.order]


    def update_graph(self,
                    generators = []):
        raise NotImplementedError

    def __str__(self) -> str:
        return [i.__str__() for i in self._elements]