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

data = ['+',4,'table','0']
details = {}

#data = kind of group, range of data, graph or table, 

@app.route('/integer/', methods=['GET', 'POST'])
def integer():
    form = integer_mod()  # Define the form here
    global data
    global details
    if request.method == 'POST':
        if (form.mod_num != None):
            try:
                if data[2] == 'table':
                    data = [str(request.form['operation']),int(request.form['mod_num']),str(request.form['graph'])]
                    details = create('Z',
                                    character=str(data[0]),
                                    size=int(data[1]))
                    colors = [choose() for i in range(data[1])]
                    k = iter(colors)
                    for i in details['elements']:
                        i.color = k.__next__()
                    return redirect(url_for('integer'),code=302)
                data = [str(request.form['operation']),int(request.form['mod_num']),str(request.form['graph']),request.form['generator'] ]
                gen = int(data[3])
                details = create('Z',
                                character=str(data[0]),
                                size=int(data[1]),
                                gen=gen)
                return redirect(url_for('integer'),code=302)

            except ValueError:
                flash('Invalid input for mod_num. Please enter a valid number.', 'error')

    form.mod_num.data = int(data[1])
    form.operation.data = data[0]
    form.graph.data = data[2]
    
    return render_template('integerm.html', 
                           title='Integer_mod_groups',
                             form=form, 
                               data=data,
                               details=details,
                               graph=0)

@app.route(
        '/symmetric/',
        methods=['GET', 'POST']
)
def symmetric():
    form = sym()
    global details
    global data
    if request.method == 'POST':
        if (form.number != None) :
            try:
                data = [str(request.form['operation']),int(request.form['number'])]  # Convert to integer
                details = create('P',
                                 character=0 if data[0] == 'S_n' else 1,
                                 size = data[1])
                colors = [choose() for i in range(len(details['elements']))]
                k = iter(colors)

                for i in details['elements']:
                    i.color = k.__next__()

                return redirect(url_for('symmetric'),code= 302)  # Redirect to the same page to see updated data
            except ValueError:
                flash('Invalid input for mod_num. Please enter a valid number.', 'error')
    
    form.number.data = data[1]

    return render_template('sym.html', 
                           title='symmetric-groups',
                             form=form, 
                               data=data
                               ,details=details)

@app.route(
        '/dihedral/',
        methods=['GET', 'POST']
)
def dihedral():
    form = dn()
    global details
    global data
    if request.method == 'POST':
        if (form.number != None) :
            try:
                data = [int(request.form['number'])]  # Convert to integer
                details = create('D',
                                 size= data[0])
                colors = [choose() for i in range(len(details['elements']))]
                k = iter(colors)
                for i in details['elements']:
                    i.color = k.__next__()
                return redirect(url_for('dihedral'),code=302)  # Redirect to the same page to see updated data
            except ValueError:
                flash('Invalid input for mod_num. Please enter a valid number.', 'error')
    form.number.data = data[0]


    return render_template('dihedral.html', 
                           title='dihedral-groups',
                             form=form, 
                               data=data
                               ,details=details)


if __name__ == '__main__':
    app.run(debug=True)