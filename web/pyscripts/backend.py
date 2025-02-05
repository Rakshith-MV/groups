import sys
import os
sys.path.append(os.getcwd().rstrip(r'\web\pyscripts'))
import groups as gp



def create(choice,*,character=None,size=None,gen=None):
    match choice:
        case 'Z':
            group = gp.Mn(size,character,gen)
            return {
                'elements': group.elements,
                'cayleys': group.cayleys(),
                'vertices': group.vertices,
                'edges': group.edges,
                'choices': group.__str__(),
                'gen':group.generators 
            }
        case 'P':
            if character == 'S_n':
                group = gp.Sn(size, 0)
            else:
                group = gp.Sn(size, 1)            
            return {
                'elements': group.elements,
                'cayleys': group.cayleys(),
                # 'conjugacy': group.compute_conjugacy_classes(),
                'vertices': group.vertices,
                'edges':group.edges
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