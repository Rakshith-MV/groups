import sys
import os

# web/pyscripts/backend.py -> repo root (two levels up), so `import groups`
# finds the top-level `groups` package regardless of the process cwd or OS.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _REPO_ROOT not in sys.path:
    sys.path.append(_REPO_ROOT)
import groups as gp


def _subgroup_data(group):
    """
    Subgroup structure for display in the info panel. Full lattice when the
    group is small enough to compute it quickly; otherwise just the cheap
    cyclic subgroups, with a flag so the template can explain why.
    """
    subs = group.subgroups()
    if subs is not None:
        return {
            'subgroups': [sorted(h.__str__() for h in H) for H in subs],
            'subgroups_capped': False,
        }
    return {
        'subgroups': [sorted(h.__str__() for h in H) for H in group.cyclic_subgroups()],
        'subgroups_capped': True,
    }


def create(choice,*,character=None,size=None,gen=None):
    match choice:
        case 'Z':
            if character == '+':
                group = gp.MnA(size,generators=gen)
            else:
                group = gp.MnM(size,generators=gen)
            return {
                'inverses': group._inverses,
                'elements': group._elements,
                'cayleys': group.cayleys(),
                'vertices': group.vertices,
                'edges': group.edges,
                'choices': group.__str__(),
                'gen':group.generators,
                'conjugacy_classes':group.conjugacy_classes(),
                **_subgroup_data(group),
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
                'gen':group._generators,
                'conjugacy_classes':group.conjugacy_classes(),
                **_subgroup_data(group),
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
                'choices':group.__str__(),
                'conjugacy_classes':group.conjugacy_classes(),
                **_subgroup_data(group),
            } 