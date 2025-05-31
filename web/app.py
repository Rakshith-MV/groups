from math import factorial
from turtle import title
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pyscripts.colors import choose 
import os
from pyscripts.forms import integer_mod, sym, dn
from pyscripts.backend import create

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
        "page": "product"
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
        if (form.mod_num != None):
            try:
                dmod['data'] = [str(request.form['operation']),int(request.form['mod_num']),str(request.form['graph']),request.form.getlist('generator')]
                try:
                    if dmod['previous'][1] == dmod['data'][1] or dmod['previous'][0] != dmod['data'][0]:
                        dmod['selected_generators'] = ['1'] if dmod['data'][0] == '+' else []
                        if dmod['data'][-1] != []:
                            dmod['selected_generators'] = dmod['data'][-1]
                    else:
                        dmod['selected_generators'] = ['1']
                    
                except:
                    dmod['selected_generators'] = ['1']
                dmod['details'] = create('Z',
                                    character=str(dmod['data'][0]),
                                    size=int(dmod['data'][1]),
                                    gen=dmod['selected_generators'])
                if dmod['data'][2] == 'table':
                    colors = [choose() for i in range(dmod['data'][1])]
                    for i, j in zip(dmod['details']['elements'],colors):
                        i.color = j 
                dmod['previous'] = dmod['data'].copy()
                return redirect(url_for('integer'),code=302)
            except ValueError:      
                flash('Invalid input for mod_num. Please enter a valid number.', 'error')
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
        if (form.number != None):
            # dn_data = [int(request.form['number']),str(request.form['graph']),request.form.getlist('generator')]
            try:
                dn_data = [int(request.form['number']),str(request.form['graph']),request.form.getlist('generator')]
                try:
                    if dn_previous[0] == dn_data[0]:
                        if dn_data[-1] != []:
                            dn_selected_generators = dn_data[-1]
                    else:
                        dn_selected_generators = ['r^1','f']
                except:
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
            except ValueError:
                flash('Invalid input for mod_num. Please enter a valid number.', 'error')
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
                print(sym_data[3])
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
    # form.generator.da ta = sym_data[3]
    return render_template('sym.html', 
                           title='symmetric-groups',
                             form=form, 
                               data=sym_data
                               ,details=sym_details)


@app.route(
        '/product/',
        methods=['GET', 'POST']
)
def product():
    return render_template('product.html',
                           title='product-groups')


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0')