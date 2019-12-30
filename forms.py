from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

# Forms - Used in templates
# HTML5 Number field is used instead of base WTForms IntegerField to get the input to render as a spinbox.


class PaydayForm(FlaskForm):
    amount = IntegerField('Amount',
                          validators=[DataRequired(), NumberRange(min=1, max=9999)],
                          render_kw={'placeholder': 'Amount', 'min': 1, 'max': 9999},
                          default=123)

    date = IntegerField('Date',
                        validators=[DataRequired(), NumberRange(min=1, max=31)],
                        render_kw={'placeholder': '1-31', 'min': 1, 'max': 31},
                        default=1)

    submit = SubmitField('Add Payday')


class BillForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)],
                       render_kw={'placeholder': 'Name', 'maxlength': 20},
                       default='Ima Bill')

    amount = IntegerField('Amount',
                          validators=[DataRequired(), NumberRange(min=1, max=9999)],
                          render_kw={'placeholder': 'Amount', 'min': 1, 'max': 9999},
                          default=123)

    date = IntegerField('Date',
                        validators=[DataRequired(), NumberRange(min=1, max=31)],
                        render_kw={'placeholder': '1-31', 'min': 1, 'max': 31},
                        default=2)

    add_bill = SubmitField('Add Bill')
    done = SubmitField('Done')


class IncomeForm(FlaskForm):
    amount = IntegerField('Amount',
                          validators=[DataRequired(), NumberRange(min=1, max=99999)],
                          render_kw={'placeholder': 'Amount', 'min': 1, 'max': 99999},
                          default=50)

    submit = SubmitField('Add Income')


class DebtForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)],
                       render_kw={'placeholder': 'Name', 'maxlength': 20},
                       default='Credit Card')

    principal = IntegerField('Principal',
                             validators=[DataRequired(), NumberRange(min=1, max=99999)],
                             render_kw={'placeholder': 'Principal', 'min': 1, 'max': 99999},
                             default=40)

    interest_rate = IntegerField('Interest Rate',
                                 validators=[DataRequired(), NumberRange(min=0, max=100)],
                                 render_kw={'placeholder': 'Interest Rate: 0-100', 'min': 0, 'max': 100})

    minimum = IntegerField('Minimum',
                           validators=[DataRequired(), NumberRange(min=0, max=99999)],
                           render_kw={'placeholder': 'Minimum', 'min': 0, 'max': 99999},
                           default=10)

    add_debt = SubmitField('Add Debt')
    # Not currently used.
    done = SubmitField('Done')
