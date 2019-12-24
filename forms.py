from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class PaydayForm(FlaskForm):
    amount = StringField('Amount', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('Add Payday')


class BillForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    amount = StringField('Amount', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    add_bill = SubmitField('Add Bill')
    done = SubmitField('Done')


class IncomeForm(FlaskForm):
    amount = StringField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Income')


class DebtForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    principal = StringField('Principal', validators=[DataRequired()])
    interest_rate = StringField('Interest Rate', validators=[DataRequired()])
    minimum = StringField('Minimum', validators=[DataRequired()])
    submit = SubmitField('Add Debt')
