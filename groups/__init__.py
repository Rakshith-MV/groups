# Import key functions/classes from submodules
from groups.dihedral.Dihedral import Dn
from groups.helpers import *
from groups.modulo.modulos import modulo as Mn
# from product_groups import DIrect_graphs
from groups.symmetric.permutations import Pgroup as Sn

# You can specify which symbols to export
__all__ = ['Dn', 'Mn', 'Sn']