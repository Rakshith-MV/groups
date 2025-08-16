import sys
import os
sys.path.append(os.getcwd().rstrip(r'\web\pyscripts'))
import groups as gp


def create(choice,*,character=None,size=None,gen=None):
    match choice:
        case 'Z':
            if character == '+':
                group = gp.MnA(size)
            else:
                group = gp.MnM(size)
            return {
                'inverses': group._inverses,
                'elements': group._elements,
                'cayleys': group.cayleys(),
                'vertices': group.vertices,
                'edges': group.edges,
                'choices': group.__str__(),
                'gen':group.generators 
            }
        case 'P':
            if character == 'S_n':
                group = gp.Sn(size,
                              0,
                              gen)
            else:
                group = gp.Sn(size,
                               1,
                               gen)         
            return {
                'inverses' : group._inverses,
                'elements': group._elements,
                'cayleys': group.cayleys(),
                'vertices': group.vertices,
                'edges':group.edges,
                'choices':group.__str__(),
                'gen':group._generators   
            }
        case 'D':
            group = gp.Dn(2*size,
                          generators=gen)
            return {
                'inverses': group._inverses,
                'elements': group._elements,
                'cayleys': group.cayleys(),
                'gen': [i.__str__() for i in group._generators],
                'vertices': group.vertices,
                'edges':group.edges,
                'choices':group.__str__()
            } 