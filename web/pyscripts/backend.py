import sys
import os
sys.path.append(os.getcwd().rstrip(r'\web\pyscripts'))
import groups as gp



def create(choice,*,character=None,size=None):
    match choice:
        case 'Z':
            group = gp.Mn(size,character)
            return {
                'elements': group.elements,
                'cayleys': group.cayleys(),
                'vertices': group.vertices,
                'edges':group.edges
            }
        case 'P':
            group = gp.Sn(size, character)
            return {
                'elements': group.elements,
                'cayleys': group.cayleys(),
                'conjugacy': group.compute_conjugacy_classes()
                # 'vertices': group.vertices(),
                # 'edges':group.edges()

            }
        case 'D':
            group = gp.Dn(size)
            return {
                'elements': group.elements,
                'cayleys': group.cayleys(),
                'conjugacy': group.compute_conjugacy_classes()
                # 'vertices': group.vertices(),
                # 'edges':group.edges()
            } 