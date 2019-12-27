from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
# from wtforms.fields.html5 import
from wtforms.validators import DataRequired, Length, NumberRange


class PaydayForm(FlaskForm):
    amount = IntegerField('Amount', validators=[DataRequired()], render_kw={'placeholder': 2})
    date = IntegerField('Date', validators=[DataRequired(), NumberRange(min=1, max=31)], default=14)
    submit = SubmitField('Add Payday')


class BillForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    amount = IntegerField('Amount', validators=[DataRequired()])
    date = IntegerField('Date', validators=[DataRequired(), NumberRange(min=1, max=31)])
    add_bill = SubmitField('Add Bill')
    done = SubmitField('Done')


class IncomeForm(FlaskForm):
    amount = IntegerField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Income')


class DebtForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    principal = IntegerField('Principal', validators=[DataRequired()])
    interest_rate = IntegerField('Interest Rate', validators=[DataRequired(), NumberRange(min=0, max=100)])
    minimum = IntegerField('Minimum', validators=[DataRequired()])
    submit = SubmitField('Add Debt')
