from sympy import gammasimp
import groups.modulo as gp
import groups.symmetric as sp
import groups.dihedralg as dg


K = dg.Dihedral(8, generators=['fr0','r1'])
G = dg.Dihedral(10)

a = sp.symmetric(3,0)
