from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
# from wtforms.fields.html5 import
from wtforms.validators import DataRequired, Length, NumberRange


class PaydayForm(FlaskForm):
    amount = IntegerField('Amount',
                          validators=[DataRequired()],
                          render_kw={'placeholder': 'Amount'})
    date = IntegerField('Date',
                        validators=[DataRequired(), NumberRange(min=1, max=31)],
                        default=14,
                        render_kw={'placeholder': 'Date: 1-31'})
    submit = SubmitField('Add Payday')


class BillForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)],
                       render_kw={'placeholder': 'Name'})
    amount = IntegerField('Amount',
                          validators=[DataRequired()],
                          render_kw={'placeholder': 'Amount'})
    date = IntegerField('Date',
                        validators=[DataRequired(), NumberRange(min=1, max=31)],
                        render_kw={'placeholder': 'Date: 1-31'})
    add_bill = SubmitField('Add Bill')
    done = SubmitField('Done')


class IncomeForm(FlaskForm):
    amount = IntegerField('Amount',
                          validators=[DataRequired()],
                          render_kw={'placeholder': 'Amount'})
    submit = SubmitField('Add Income')


class DebtForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)],
                       render_kw={'placeholder': 'Name'})
    principal = IntegerField('Principal',
                             validators=[DataRequired()],
                             render_kw={'placeholder': 'Principal'})
    interest_rate = IntegerField('Interest Rate',
                                 validators=[DataRequired(), NumberRange(min=0, max=100)],
                                 render_kw={'placeholder': 'Interest Rate: 0-100'})
    minimum = IntegerField('Minimum',
                           validators=[DataRequired()],
                           render_kw={'placeholder': 'Minimum'})
    submit = SubmitField('Add Debt')
