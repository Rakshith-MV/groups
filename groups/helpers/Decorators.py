from itertools import chain, combinations
from functools import cache

#groups may not exceed this, if in case then use the prime function.
primes = (2,3,4,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199)
"""
This is a custom cache decorator for multiply method, it may be usefull to form structures of the group in the long run, which might include 
multiple product operations
"""

__init__ = """This is a custom cache decorator for multiply method,
             it may be usefull to form structures of the group in the long run,
             which might include multiple product operations
            """

__all__ = ["custom_cache", "class_cache","unitary"]

def custom_cache(f):
    cache = {}
    def wrappers(a,
                 b
                 )->any:
        hash = ""
        hash = a.__str__() + b.__str__()
        if hash in cache:
            return cache[hash]
        obj = f(a,b)

        cache[hash] = obj
        return obj
    return wrappers


def class_cache(c):
    cache = {}
    def wrapper(group_order: int,
            element :any,
            init_inverse :bool = False
            ):
        if type(element) == str:
            string = element
            hash = str(group_order)+element
            maps = _strtomap(group_order
                             ,element)
        elif type(element) == dict:
            maps = element
            string = _maptostr(group_order, 
                               element)
            hash =  str(group_order) + string
        
        else:
            raise IOError ("Either a string or a dictionary \n notin fancy")

        if hash in cache:
            return cache[hash]
        obj = c(group_order, string, maps)
        cache[hash] = obj

        return obj    
    return wrapper


#Helper functions:
# -----------------------------------------------------------------------------------------------------
def _strtomap(n:int,
                element: str
                )->dict:
    """ 
    Creates a dict of mapping.
    input: string of permutamdons(separated by commas to indicate cycles)
    ouput: Dictionary of mappings, 
    """
    values = [str(i) for i in range(n)]
    D = dict(zip(values, values))
    for i in element:
        l = len(i)
        for k in range(l):
            D[i[k]] = i[(k+1)%l]
    return D

def _maptostr(n,
                D:dict
                )->str:
    """
    Takes in a dictionary of mapping, produces a list of disjoint strings.

    """
    l = []
    new_string = "0"
    values = [str(i) for i in range(n)]
    output_str = ""
    while(True):
        try:
            if D[new_string[-1]] !=new_string[0]:        #To check for cycle completion
                values.remove(new_string[-1])            #remove the previous value from the list
                new_string+= D[new_string[-1]]                 
            else:
                values.remove(new_string[-1])
                if len(new_string) != 1:
                    output_str+=(new_string+',')
                if len(values) == 0:
                    break
                new_string = values[0]
        except:
            assert ValueError ("Doesn't form a proper cycles. ")
            return None
    
    return output_str.rstrip(',')

def even(
        s:object
        )->bool:
    sum = 0
    for i in s.string.split(','):
        sum += (len(i)%2)
    if sum == 0:
        return 1
    return sum%2

#-----------------------------------------------------------------------------------------------------------------

@cache
def unitary(n:int
            )->list:
    m = [i for i in range(1,n)]
    def coprime(a:int,
                b:int):
        for i in range(2,a+1):
            if a%i == 0 and b%i==0:
                return 0
        return 1
    
    for i in m[1:]:
        if coprime(i,n) == 0:
            mul = 1
            while(mul*i < n):
                try:
                    m.remove(mul*i)
                except:
                    None
                mul+=1
    return m


#seems to be most optimal, using sets of numbers and indexing might be much faster
@cache
def powerset(
            n:int
            ):
    s = range(n)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

@cache
def prime_decomposition(
        k:int
        ):
    i = 0
    factors = {}
    while k != 1:
        if k%primes[i]  == 0:
            k = k//primes[i]
            if primes[i] not in factors.keys():
                factors[primes[i]] = 1
            else:
                factors[primes[i]]+=1
        else:
            i+=1
    return factors
    