from .modulo import ModuloA as MnA
from .modulo import ModuloM as MnM
from .dihedralg import Dihedral as Dn
from .symmetric import symmetric as Sn
from .isomorphism import is_isomorphic as iso
# You can specify which symbols to export
__all__ = ['Dn', 'MnA', 'Sn', 'MnM', 'iso']