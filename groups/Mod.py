from functools import cache
import math
from .group_base import Group, element
from .graphs import circle
from .Decorators import unitary


class modA(Group):
    def __init__(self,
                 n:int,
                 generators:list=[]
                 ):
        super().__init__(n)




class elementsA(elements):
    ...