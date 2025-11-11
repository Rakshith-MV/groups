from groups.symmetric import symmetric as Sn
from groups.dihedralg import Dihedral as Dn


K = Dn(8)
for i in K.conjugacy_classes():
    for j in i:
        print(j,end=', ')
    print()