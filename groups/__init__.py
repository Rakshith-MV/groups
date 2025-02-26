# Import key functions/classes from submodules
from groups.dihedral.Dihedral import Dn
from groups.helpers import *
from groups.modulo.modulos import modulo as Mn
from groups.product_groups.product import Pn
from groups.symmetric.permutation_groups import Sn

# You can specify which symbols to export
__all__ = ['Dn', 'Mn', 'Sn','Pn']