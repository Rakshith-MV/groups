from re import L


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

    def __eq__(self, value):
        """
        Naive as of now
        """
        if isinstance(value, element):
            return self._number == value._number
        return False

    def __hash__(self):
        try:
            return hash(self._number)
        except:
            return hash(self._string)

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
        self._generators = [i for i in self._elements if i._order == self._order]
    
    def cycles(self,
               j):
        if isinstance(j, element):
            return [i*j for i in self._elements]
        else:
            raise TypeError("Input must be an instance of the element class.")


    def update_graph(self,
                    generators = []):
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self._order)
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self._elements[key]
        elif isinstance(key, str):
            return next((i for i in self._elements if i.__str__() == key), None)
        else:
            raise TypeError("Key must be an integer or a string representing the element.")

    def __iter__(self):
        return iter(self._elements)

    def __str__(self) -> list:
        return [i.__str__() for i in self._elements]