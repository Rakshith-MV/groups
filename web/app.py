from math import factorial, gcd
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pyscripts.colors import choose 
import os
import sys
import math
from pyscripts.forms import integer_mod, sym, dn, product_group_form
from pyscripts.backend import create

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.append(_REPO_ROOT)
import groups as gp

app = Flask(__name__)




# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'cayley'
# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Sample data - in a real app, this might come from a database
groups = [
    {
        "id": 1,
        "name": "Modulo",
        "description": "Mathematics group dealing with modular arithmetic",
        "color": "#1DA1F2",
        "image": "modulos.png",
        "page": "integer"
    },
    {
        "id": 2,
        "name": "Dihedral",
        "description": "Geometric symmetry groups",
        "color": "#1DA1F2",
        "image": "dihedral.png",
        "page": "dihedral"

    },
    {
        "id": 3,
        "name": "Symmetric",
        "description": "Permutation groups",
        "color": "#1DA1F2",
        "image": "symmetric.jpeg",
        "page": "symmetric"

    },
    {
        "id": 4,
        "name": "Product groups",
        "description": "General group theory",
        "color": "#1DA1F2",
        "image": "symetric.png",
        "page": "product"
    }
    ,
    {
        "id": 5,
        "name": "Mappings",
        "description": "Isomorphisms and Homomorphisms",
        "color": "#1DA1F2",
        "image": "maps.png",
        "page": "mappings"
    }
]

@app.route('/')
@app.route('/home', methods=[
    'POST'])
def home():
    return render_template('index.html', groups=groups)

#dmod['data']= kind of group, range of data, graph or table,
dmod = {'data':['+',4,'table','0'],
        'details':{},
        'previous':{},
        'selected_generators': []
}

#sym_data = ['type',number, graph]
sym_data = ['S_n',3,'table',None]
sym_details = {}
sym_previous = []
sym_selected_generators = []


dn_data = [3,'table']
dn_details = {}
dn_dn_selected_generators = ['f','r^1']
dn_previous = [] 

@app.route('/integer/', methods=['GET', 'POST'])
def integer():
    form = integer_mod()  # Define the form here
    global dmod
    if request.method == 'POST':
        dmod['data'] = [str(request.form['operation']),int(request.form['mod_num']),str(request.form['graph']),request.form.getlist('generator')]
        if dmod['data'][-1] == [] or dmod['data'][-1] == None:
            dmod['selected_generators'] = ['1']
        else:
            dmod['selected_generators'] = dmod['data'][-1]

        dmod['details'] = create('Z',
                            character=str(dmod['data'][0]),
                            size=int(dmod['data'][1]),
                            gen=dmod['selected_generators'])

        if dmod['data'][2] == 'table':
            colors = [choose() for i in range(dmod['data'][1])]
            for i, j in zip(dmod['details']['elements'],colors):
                i.color = j 
        dmod['previous'] = dmod['data'].copy()
        return redirect(url_for('integer'), code=302)
    
    form.mod_num.data = int(dmod['data'][1])    
    form.operation.data = dmod['data'][0]
    form.graph.data = dmod['data'][2]
    return render_template('integerm.html',
                            title='Integer_mod_groups',
                            form=form,
                            data=dmod['data'],
                            details=dmod['details'],
                            graph=0)

@app.route(
        '/dihedral/',
        methods=['GET', 'POST']
)
def dihedral():    
    form = dn()
    global dn_details
    global dn_data
    global dn_selected_generators    #is this necessary 
    global dn_previous
    if request.method == 'POST':
        dn_data = [int(request.form['number']),str(request.form['graph']),request.form.getlist('generator')]
        try:
            if dn_previous[0] == dn_data[0]:
                if dn_data[-1] != []:
                    dn_selected_generators = dn_data[-1]
            else:
                dn_selected_generators = ['r^1','f']
        except IndexError:
            # dn_previous is empty on the very first request
            dn_selected_generators = ['r^1','f']
        dn_details = create('D',
                            size= dn_data[0],
                            gen=dn_selected_generators)
        if dn_data[1] == 'table':
            colors = [choose() for i in range(len(dn_details['elements']))]
            for i,j in zip(dn_details['elements'],colors):
                i.color = j
        dn_previous = dn_data.copy()
        return redirect(url_for('dihedral'),code=302)  # Redirect to the same page to see updated data

    form.number.data = dn_data[0]
    form.graph.data = dn_data[1]
    return render_template('dihedral.html', 
                           title='dihedral-groups',
                             form=form, 
                               data=dn_data,
                               details=dn_details)
 
@app.route(
        '/symmetric/',
        methods=['GET', 'POST']
)
def symmetric():
    form = sym()
    global sym_details
    global sym_data
    if request.method == 'POST':
        if (form.number != None) :
            try:
                sym_data = [str(request.form['operation']),int(request.form['number']),str(request.form['graph']),request.form.getlist('generator')]
                sym_details = create('P',
                                 character= sym_data[0],
                                 size = sym_data[1],
                                 gen=sym_data[3])
                colors = [choose() for i in range(len(sym_details['elements']))]
                k = iter(colors)
                for i in sym_details['elements']:
                    i.color = k.__next__()
                return redirect(url_for('symmetric'),code= 302)  # Redirect to the same page to see updated data
            except ValueError:
                flash('Invalid input for mod_num. Please enter a valid number.', 'error')
    
    form.operation.data = sym_data[0]
    form.number.data = sym_data[1]
    form.graph.data = sym_data[2]
    # form.generator.data = sym_data[3]
    return render_template('sym.html',
                           title='symmetric-groups',
                             form=form, 
                               data=sym_data
                               ,details=sym_details)

prod_data = {
    'g1_type': 'Z', 'g1_op': '+', 'g1_size': 2,
    'g2_type': 'Z', 'g2_op': '+', 'g2_size': 3,
    'g3_type': 'None', 'g3_op': '+', 'g3_size': 2,
    'graph': 'table',
    'selected_generators': []
}
prod_details = {}
prod_previous = {}

@app.route('/product/', methods=['GET', 'POST'])
def product():
    form = product_group_form()
    global prod_data, prod_details, prod_previous
    
    if not prod_details:
        character = [('Z', 2, '+'), ('Z', 3, '+')]
        prod_details = create('Product', character=character, gen=[])
        prod_data['selected_generators'] = prod_details['gen']

    if request.method == 'POST':
        g1_type = request.form.get('g1_type')
        g1_op = request.form.get('g1_op')
        g1_size = int(request.form.get('g1_size', 2))

        g2_type = request.form.get('g2_type')
        g2_op = request.form.get('g2_op')
        g2_size = int(request.form.get('g2_size', 2))

        g3_type = request.form.get('g3_type')
        g3_op = request.form.get('g3_op')
        g3_size = int(request.form.get('g3_size', 2))

        graph_type = request.form.get('graph', 'table')
        generators = request.form.getlist('generator')

        character = [(g1_type, g1_size, g1_op)]
        if g2_type != 'None':
            character.append((g2_type, g2_size, g2_op))
        if g3_type != 'None':
            character.append((g3_type, g3_size, g3_op))

        computed_order = 1
        for c in character:
            if c[0] == 'Z':
                if c[2] == '+':
                    computed_order *= c[1]
                else:
                    u_size = len([i for i in range(1, c[1] + 1) if math.gcd(i, c[1]) == 1])
                    computed_order *= u_size
            elif c[0] == 'D':
                computed_order *= (2 * c[1])
            elif c[0] == 'S':
                import math as pymath
                fact = pymath.factorial(c[1])
                if c[2] == 'S_n':
                    computed_order *= fact
                else:
                    computed_order *= (fact // 2)

        if computed_order > 60:
            flash(f"Requested product group has order {computed_order}, which is too large. Please keep total size <= 60.", 'error')
            return redirect(url_for('product'), code=302)

        prod_data = {
            'g1_type': g1_type, 'g1_op': g1_op, 'g1_size': g1_size,
            'g2_type': g2_type, 'g2_op': g2_op, 'g2_size': g2_size,
            'g3_type': g3_type, 'g3_op': g3_op, 'g3_size': g3_size,
            'graph': graph_type,
            'selected_generators': generators
        }

        components_changed = False
        prev_char = prod_previous.get('character')
        if prev_char != character:
            components_changed = True

        if components_changed or not generators:
            prod_details = create('Product', character=character, gen=None)
            prod_data['selected_generators'] = prod_details['gen']
        else:
            prod_details = create('Product', character=character, gen=generators)
            prod_data['selected_generators'] = generators

        prod_previous = {'character': character}
        return redirect(url_for('product'), code=302)

    form.g1_type.data = prod_data.get('g1_type', 'Z')
    form.g1_op.data = prod_data.get('g1_op', '+')
    form.g1_size.data = prod_data.get('g1_size', 2)

    form.g2_type.data = prod_data.get('g2_type', 'Z')
    form.g2_op.data = prod_data.get('g2_op', '+')
    form.g2_size.data = prod_data.get('g2_size', 3)

    form.g3_type.data = prod_data.get('g3_type', 'None')
    form.g3_op.data = prod_data.get('g3_op', '+')
    form.g3_size.data = prod_data.get('g3_size', 2)

    form.graph.data = prod_data.get('graph', 'table')

    title_parts = []
    g1_lbl = f"Z_{prod_data.get('g1_size')}" if prod_data.get('g1_type') == 'Z' else (f"D_{prod_data.get('g1_size')}" if prod_data.get('g1_type') == 'D' else f"S_{prod_data.get('g1_size')}")
    title_parts.append(g1_lbl)
    if prod_data.get('g2_type') != 'None':
        g2_lbl = f"Z_{prod_data.get('g2_size')}" if prod_data.get('g2_type') == 'Z' else (f"D_{prod_data.get('g2_size')}" if prod_data.get('g2_type') == 'D' else f"S_{prod_data.get('g2_size')}")
        title_parts.append(g2_lbl)
    if prod_data.get('g3_type') != 'None':
        g3_lbl = f"Z_{prod_data.get('g3_size')}" if prod_data.get('g3_type') == 'Z' else (f"D_{prod_data.get('g3_type')}" if prod_data.get('g3_type') == 'D' else f"S_{prod_data.get('g3_size')}")
        title_parts.append(g3_lbl)
    group_title = " × ".join(title_parts)

    return render_template('product.html',
                           title='product-groups',
                           form=form,
                           data=[group_title, prod_data.get('graph')],
                           details=prod_details)


def get_group_instance(g_type, size, op):
    size = int(size)
    if g_type == 'Z':
        if op == '+':
            return gp.MnA(size)
        else:
            return gp.MnM(size)
    elif g_type == 'D':
        return gp.Dn(2 * size)
    elif g_type == 'S':
        if op == 'S_n':
            return gp.Sn(size, 0)
        else:
            return gp.Sn(size, 1)
    return None

def find_homomorphisms(G_obj, H_obj, K_elements_str_set):
    from web.pyscripts.backend import _find_generators
    gens = _find_generators(G_obj, G_obj._elements)
    gens_list = list(gens)
    
    import itertools
    homomorphisms = []
    H_elements = H_obj._elements
    
    for combo in itertools.product(H_elements, repeat=len(gens_list)):
        gen_mapping = dict(zip(gens_list, combo))
        
        mapping = {}
        mapping[G_obj._identity] = H_obj._identity
        
        queue = [G_obj._identity]
        possible = True
        
        while queue:
            current = queue.pop(0)
            for gen in gens_list:
                nxt = current * gen
                nxt_val = mapping[current] * gen_mapping[gen]
                if nxt in mapping:
                    if mapping[nxt] != nxt_val:
                        possible = False
                        break
                else:
                    mapping[nxt] = nxt_val
                    queue.append(nxt)
            if not possible:
                break
                
        if possible and len(mapping) == len(G_obj._elements):
            for a in G_obj._elements:
                for b in G_obj._elements:
                    if mapping[a * b] != mapping[a] * mapping[b]:
                        possible = False
                        break
                if not possible:
                    break
            
            if possible:
                kernel = {g for g, img in mapping.items() if img == H_obj._identity}
                kernel_str_set = {str(k) for k in kernel}
                
                if kernel_str_set == K_elements_str_set:
                    map_dict = {str(k): str(v) for k, v in mapping.items()}
                    is_injective = (len(kernel) == 1)
                    image = set(mapping.values())
                    is_surjective = (len(image) == len(H_elements))
                    is_bijective = (is_injective and is_surjective)
                    
                    homomorphisms.append({
                        'mapping': map_dict,
                        'is_injective': is_injective,
                        'is_surjective': is_surjective,
                        'is_bijective': is_bijective,
                        'image_size': len(image),
                    })
                    
    return homomorphisms

def get_group_details(g_type, size, op):
    size = int(size)
    if g_type == 'Z':
        return create('Z', character=op, size=size)
    elif g_type == 'D':
        return create('D', size=size)
    elif g_type == 'S':
        return create('P', character=op, size=size)
    return None

@app.route('/mappings/', methods=['GET', 'POST'])
def mappings():
    if request.method == 'POST':
        dom_type = request.form.get('dom_type')
        dom_op = request.form.get('dom_op')
        dom_size = int(request.form.get('dom_size', 4))

        codom_type = request.form.get('codom_type')
        codom_op = request.form.get('codom_op')
        codom_size = int(request.form.get('codom_size', 2))

        if dom_size > 32 or codom_size > 32:
            flash("For mappings visualization, please keep both groups size <= 32.", 'error')
            return redirect(url_for('mappings'))

        try:
            dom_group = get_group_instance(dom_type, dom_size, dom_op)
            codom_group = get_group_instance(codom_type, codom_size, codom_op)
        except Exception as e:
            flash(f"Error creating groups: {e}", 'error')
            return redirect(url_for('mappings'))

        if not dom_group or not codom_group:
            flash("Could not create selected groups.", 'error')
            return redirect(url_for('mappings'))

        normal_subs = []
        subs = dom_group.subgroups()
        if subs:
            for H in subs:
                if dom_group.is_normal(H):
                    normal_subs.append({
                        'elements': sorted(h.__str__() for h in H),
                        'order': len(H),
                        'normal': True,
                        'cosets': [sorted(e.__str__() for e in c) for c in dom_group.cosets(H, side='left')],
                    })
        
        normal_subs = sorted(normal_subs, key=lambda x: x['order'])

        dom_elements = [str(e) for e in dom_group._elements]
        codom_elements = [str(e) for e in codom_group._elements]

        dom_details = get_group_details(dom_type, dom_size, dom_op)
        codom_details = get_group_details(codom_type, codom_size, codom_op)

        dom_cayleys = [[str(cell) for cell in row] for row in dom_details['cayleys']] if dom_details and 'cayleys' in dom_details else []
        codom_cayleys = [[str(cell) for cell in row] for row in codom_details['cayleys']] if codom_details and 'cayleys' in codom_details else []

        dom_vertices = dom_details.get('vertices', []) if dom_details else []
        dom_edges = dom_details.get('edges', {}) if dom_details else {}
        codom_vertices = codom_details.get('vertices', []) if codom_details else []
        codom_edges = codom_details.get('edges', {}) if codom_details else {}

        return render_template('mappings.html',
                               title='mappings',
                               normal_subgroups=normal_subs,
                               dom_elements=dom_elements,
                               codom_elements=codom_elements,
                               dom_cayleys=dom_cayleys,
                               codom_cayleys=codom_cayleys,
                               dom_vertices=dom_vertices,
                               dom_edges=dom_edges,
                               codom_vertices=codom_vertices,
                               codom_edges=codom_edges,
                               dom_config=(dom_type, dom_op, dom_size),
                               codom_config=(codom_type, codom_op, codom_size))

    return render_template('mappings.html',
                           title='mappings',
                           normal_subgroups=None,
                           dom_elements=[],
                           codom_elements=[],
                           dom_cayleys=[],
                           codom_cayleys=[],
                           dom_vertices=[],
                           dom_edges={},
                           codom_vertices=[],
                           codom_edges={},
                           dom_config=None,
                           codom_config=None)

@app.route('/mappings/api/homomorphisms/', methods=['POST'])
def api_homomorphisms():
    data = request.json
    dom_type = data.get('dom_type')
    dom_op = data.get('dom_op')
    dom_size = data.get('dom_size')

    codom_type = data.get('codom_type')
    codom_op = data.get('codom_op')
    codom_size = data.get('codom_size')
    
    kernel_index = data.get('kernel_index')

    dom_group = get_group_instance(dom_type, dom_size, dom_op)
    codom_group = get_group_instance(codom_type, codom_size, codom_op)

    if not dom_group or not codom_group:
        return jsonify({'homomorphisms': []})

    normal_subs = []
    subs = dom_group.subgroups()
    if subs:
        for H in subs:
            if dom_group.is_normal(H):
                normal_subs.append(H)
    normal_subs = sorted(normal_subs, key=len)

    if kernel_index < 0 or kernel_index >= len(normal_subs):
        return jsonify({'homomorphisms': []})

    K_sub = normal_subs[kernel_index]
    K_str_set = {str(k) for k in K_sub}

    homs = find_homomorphisms(dom_group, codom_group, K_str_set)
    return jsonify({'homomorphisms': homs})


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0')