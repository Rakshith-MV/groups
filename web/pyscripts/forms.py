from tkinter import Widget
from typing import Self
from flask_wtf import FlaskForm
from wtforms import RadioField, IntegerField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import CheckboxInput, ColorInput, ListWidget, TableWidget, Option

class integer_mod(FlaskForm):
    graph = RadioField('Viz',choices=['graph','table'],default='table')
    operation = RadioField('Operation',choices=['+','*'],default='+')
    mod_num = IntegerField(validators=[DataRequired(),NumberRange(1,30,'Number b/w 0-30 please!!')],default=None)
    submit = SubmitField('compute')
    generator = SelectMultipleField('Choose Generator', 
                                    choices=[],
                                    default=None,
                                    id="GeneratorField",
                                    option_widget=CheckboxInput(),
                                    widget=ListWidget(prefix_label=False)
                                    )
    
    # #Don't know how this is not working..!!   
    # def update(self,data):  
    #     self.generator.data = data
    #     return ''  # Return empty string to prevent printing


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
    generator = SelectMultipleField("Choose Generator", 
                          choices=[], 
                          default=None,
                          id="GeneratorField",
                          option_widget=CheckboxInput(),
                          widget=ListWidget(prefix_label=False)
                        )

    def update(self,data):
        self.generator.data = data
        return ''

if __name__  == '__main__':
    print(help(SelectField))