from math import factorial
from flask import Flask, render_template, request, redirect, url_for, session, flash
from wtforms import SelectField
from pyscripts.colors import choose 
import os
from werkzeug.utils import secure_filename
from pyscripts.forms import integer_mod, sym, dn
from pyscripts.backend import create
import random
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
        "page": "integer"
    }
]

@app.route('/')
@app.route('/home', methods=[
    'POST'])
def home():
    return render_template('index.html', groups=groups)

#int_data = kind of group, range of data, graph or table,
int_data = ['+',4,'table','0']
int_details = {}
#sym_data = ['type',number, graph]
sym_data = ['S_n',3,'table',None]
sym_details = {}

dn_data = [3,'table']
dn_details = {}

 

@app.route('/integer/', methods=['GET', 'POST'])
def integer():
    form = integer_mod()  # Define the form here
    global int_data
    global int_details
    if request.method == 'POST':
        if (form.mod_num != None):
            try:
                if int_data[2] == 'table':
                    int_data = [str(request.form['operation']),int(request.form['mod_num']),str(request.form['graph'])]
                    int_details = create('Z',
                                    character=str(int_data[0]),
                                    size=int(int_data[1]))
                    colors = [choose() for i in range(int_data[1])]
                    k = iter(colors)
                    for i in int_details['elements']:
                        i.color = k.__next__()
                    return redirect(url_for('integer'),code=302)
                int_data = [str(request.form['operation']),int(request.form['mod_num']),str(request.form['graph']),request.form['generator'] ]
                gen = int(int_data[3])
                int_details = create('Z',
                                character=str(int_data[0]),
                                size=int(int_data[1]),
                                gen=gen)
                return redirect(url_for('integer'),code=302)

            except ValueError:
                flash('Invalid input for mod_num. Please enter a valid number.', 'error')

    
    form.mod_num.data = int(int_data[1])
    form.operation.data = int_data[0]
    form.graph.data = int_data[2]
    
    return render_template('integerm.html', 
                           title='Integer_mod_groups',
                             form=form, 
                               data=int_data,
                               details=int_details,
                               graph=0)

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
                sym_data = [str(request.form['operation']),int(request.form['number']),str(request.form['graph'])]  # Convert to integer
                sym_details = create('P',
                                 character= sym_data[0],
                                 size = sym_data[1])
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

@app.route(
        '/dihedral/',
        methods=['GET', 'POST']
)
def dihedral():
    form = dn()
    global dn_details
    global dn_data
    if request.method == 'POST':
        if (form.number != None):
            try:
                dn_data = [int(request.form['number']),str(request.form['graph'])]  # Convert to integer
                dn_details = create('D',
                                 size= dn_data[0])
                colors = [choose() for i in range(len(dn_details['elements']))]
                k = iter(colors)
                for i in dn_details['elements']:
                    i.color = k.__next__()
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


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')