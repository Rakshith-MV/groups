from flask_wtf import FlaskForm
from wtforms import RadioField, IntegerField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import CheckboxInput, ColorInput, ListWidget, TableWidget, Option

class integer_mod(FlaskForm):
    graph = RadioField('Viz',choices=['graph','table','info'],default='table')
    operation = RadioField('Operation',choices=['+','*'],default='+')
    mod_num = IntegerField(validators=[DataRequired(),NumberRange(1,30,'Number b/w 0-30 please!!')],default=None)
    submit = SubmitField('compute')
    generator = SelectMultipleField('Choose Generator', 
                                    choices=[],
                                    default=None,
                                    id="GeneratorField"
                                    )


class sym(FlaskForm):
    graph = RadioField('Viz',choices=['graph','table','info'],default='table')
    operation = RadioField('S/A',choices=['S_n','A_n'],default='S_n')
    number = IntegerField(validators=[DataRequired(), NumberRange(1,5,'Number b/w 1-5 please!!')],default=None)
    submit = SubmitField('compute')
    generator = SelectMultipleField("Choose Generator", 
                                    choices=[], 
                                    default=None, 
                                    id="GeneratorField"
    )

    def update(self,data):
        self.generator.data = data
        return ''


class dn(FlaskForm):
    graph = RadioField('Viz',choices=['graph','table','info'],default='table')
    number = IntegerField(validators=[DataRequired(), NumberRange(1,15,'Number b/w 1-15 please!!')],default=3)
    submit = SubmitField('compute')
    generator = SelectMultipleField("Choose Generator", 
                          choices=[], 
                          default=None,
                          id="GeneratorField"
                        )

    def update(self,data):
        self.generator.data = data
        return ''

class product_group_form(FlaskForm):
    graph = RadioField('Viz',choices=['graph','table','info'],default='table')
    
    g1_type = SelectField('Group 1 Type', choices=[('Z', 'Modulo'), ('D', 'Dihedral'), ('S', 'Symmetric')], default='Z')
    g1_op = SelectField('Group 1 Op/Type', choices=[('+', '+'), ('*', '*'), ('S_n', 'S_n'), ('A_n', 'A_n')], default='+')
    g1_size = IntegerField('Group 1 Size/n', validators=[DataRequired(), NumberRange(1, 15, '1-15 please')], default=2)

    g2_type = SelectField('Group 2 Type', choices=[('None', 'None'), ('Z', 'Modulo'), ('D', 'Dihedral'), ('S', 'Symmetric')], default='None')
    g2_op = SelectField('Group 2 Op/Type', choices=[('+', '+'), ('*', '*'), ('S_n', 'S_n'), ('A_n', 'A_n')], default='+')
    g2_size = IntegerField('Group 2 Size/n', default=2)

    g3_type = SelectField('Group 3 Type', choices=[('None', 'None'), ('Z', 'Modulo'), ('D', 'Dihedral'), ('S', 'Symmetric')], default='None')
    g3_op = SelectField('Group 3 Op/Type', choices=[('+', '+'), ('*', '*'), ('S_n', 'S_n'), ('A_n', 'A_n')], default='+')
    g3_size = IntegerField('Group 3 Size/n', default=2)

    submit = SubmitField('compute')
    generator = SelectMultipleField("Choose Generator", 
                          choices=[], 
                          default=None,
                          id="GeneratorField"
                        )

    def update(self,data):
        self.generator.data = data
        return ''

if __name__  == '__main__':
    print(help(SelectField))

