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
                'elements': group.elements,
                'cayleys': group.cayleys(),
                'vertices': group.vertices,
                'edges':group.edges,
                'choices':group.names,
                'gen':group.generators   
            }
        case 'D':
            group = gp.Dn(size, gen=gen)
            return {
                'elements': group.elements,
                'cayleys': group.cayleys(),
                # 'conjugacy': group.compute_conjugacy_classes()
                'gen':group.generators,
                'vertices': group.vertices,
                'edges':group.edges,
                'choices':group.__str__()
            } 