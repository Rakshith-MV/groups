from flask_wtf import FlaskForm
from wtforms import RadioField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange

class integer_mod(FlaskForm):
    graph = RadioField('Viz',choices=['graph','table'],default='table')
    operation = RadioField('Operation',choices=['+','*'],default='+')
    mod_num = IntegerField(validators=[DataRequired(),NumberRange(1,30,'Number b/w 0-30 please!!')],default=None)
    submit = SubmitField('compute')
    generator = SelectField('Choose Generator', choices=[], default=10)
        
    #Don't know how this is not working..!!
    def update(self,data):
        self.generator.data = data
        return ''  # Return empty string to prevent printing


class sym(FlaskForm):
    graph = RadioField('Viz',choices=['graph','table'],default='table')
    operation = RadioField('S/A',choices=['S_n','A_n'],default='S_n')
    number = IntegerField(validators=[DataRequired(), NumberRange(1,5,'Number b/w 1-5 please!!')],default=None)
    submit = SubmitField('compute')
    generator = SelectField("Choose Generator", choices=[], default=None)

    def update(self,data):
        self.generator.data = data
        return ''


class dn(FlaskForm):
    graph = RadioField('Viz',choices=['graph','table'],default='table')
    number = IntegerField(validators=[DataRequired(), NumberRange(1,15,'Number b/w 1-15 please!!')],default=3)
    submit = SubmitField('compute')
    generator = SelectField("Choose Generator", choices=[], default=None)