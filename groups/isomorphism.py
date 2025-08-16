from .dihedralg import Dihedral as Dn
from .symmetric import symmetric as Sn
from .modulo import ModuloA as MnA
from .modulo import ModuloA as MnM


def is_isomorphic(G1, 
                  G2
                  )-> bool:
    """
    Check if two groups are isomorphic. 
    """
    one , two = type(G1), type(G2)
    if G1._order != G2._order:
        return False
    # Dihedral and Dihedral    
    if isinstance(G1, Dn) and isinstance(G2, Dn):
        return True
    # Symmetric and Symmetric
    elif isinstance(G1, Sn) and isinstance(G2, Sn):
        return True
    # Modulo A and Modulo A
    elif isinstance(G1, MnA) and isinstance(G2, MnA):
        return True
    # Modulo M and Modulo M
    elif isinstance(G1, MnM) and isinstance(G2, MnM):
        return True

    # Dihedral and Modulo A
    elif (isinstance(G1, Dn) and isinstance(G2, MnA)) or (isinstance(G1,MnA) and isinstance(G2, Dn)):
        return False
    # Dihedral and Modulo M
    elif (isinstance(G1, Dn) and isinstance(G2, MnM)) or (isinstance(G1,MnM) and isinstance(G2, Dn)):
        return False
    # Symmetric and Modulo A
    elif (isinstance(G1, Sn) and isinstance(G2, MnA)) or (isinstance(G1,MnA) and isinstance(G2, Sn)):
        ...
    # Symmetric and Modulo M
    elif (isinstance(G1, Sn) and isinstance(G2, MnM)) or (isinstance(G1,MnM) and isinstance(G2, Sn)):
        ...
    # Modulo A and Modulo M
    elif (isinstance(G1, MnA) and isinstance(G2, MnM)) or (isinstance(G1,MnM) and isinstance(G2, MnA)):
        ...
    elif (isinstance(G1, Sn) and isinstance(G2, Dn)) or (isinstance(G1,Dn) and isinstance(G2, Sn)):
        ...
    else:
        return False


def test():
    """
    Test the is_isomorphic function.
    """
    G1 = Dn(6)
    G2 = Dn(6)
    G3 = MnA(3)
    G4 = MnA(3)

    print(is_isomorphic(G1, G2))  # Should return True
    print(is_isomorphic(G1, G4))  # Should return False
    print(is_isomorphic(G3, G4))  # Should return False