from flask import Flask, render_template, redirect, url_for, session, request
from forms import BillForm, PaydayForm, IncomeForm, DebtForm
import bills
import debts

app = Flask(__name__)

# Secret key is required for all encryption.
# A dummy key is currently being used for development.
# Will be swapped to a key set via environmental variable or some shits for security.
app.config['SECRET_KEY'] = 'dev'


# TODO: Implement this helper function
def deserialize_to_list(session_list, new_list):
    pass


def to_json(some_item):
    return some_item.__dict__


# TODO: Test This
# Helper function to append to lists within the section dictionary.
# Was having trouble accessing the lists directly. Probably do to some underlying implementation detail of sessions.
def session_append(session_list, apendee):
    temp = session_list
    temp.append(apendee)
    return temp


# TODO: Test this
# Helper function to strip excess whitespace from object names.
def strip_whitespace(some_string):
    return " ".join(some_string.split())


# Routes

# Home/index route. Not sure if should call it index in flask.
# Clears current session and creates some session lists as setup.
@app.route('/')
@app.route('/home')
def home():
    session.clear()
    session['bills'] = []
    session['debts'] = []
    return render_template('home.html')


# Route for adding payday objects. If input validates, a PayDay object is created.
# The object is then serialized into json. The route has logic to determine how many paydays have been added.
# Route redirects after two paydays have been added.
@app.route('/payday', methods=['POST', 'GET'])
def payday():
    form = PaydayForm()
    if form.validate_on_submit():
        amount = form.amount.data
        date = form.date.data
        temp = bills.PayDay(amount, date)

        if 'paydays' not in session:
            session['paydays'] = []
            session['paydays'] = session_append(session['paydays'], to_json(temp))

            return redirect(url_for('payday'))
        else:
            session['paydays'] = session_append(session['paydays'], to_json(temp))

            return redirect(url_for('bill'))

    return render_template('payday.html', title='Payday', form=form)


# Route for adding bill objects. If input validates, a Bill object is created.
# The object is then serialized into json and added to the session.
# The route employs a form with two submit buttons. One is used for submission, while the other is used as a done flag.
# Route redirects on 'done' flag without validating or submitting current data.
@app.route('/bill', methods=['POST', 'GET'])
def bill():
    form = BillForm()
    if request.method == 'POST':
        if form.done.data is True:
            return redirect(url_for('bill_output'))

    if form.validate_on_submit():
        name = strip_whitespace(form.name.data)
        amount = form.amount.data
        date = form.date.data
        temp = bills.Bill(name, amount, date)
        session['bills'] = session_append(session['bills'], to_json(temp))

        return redirect(url_for('bill'))

    return render_template('bill.html', title='bill', form=form,
                           p1a=session['paydays'][0]['amount'], p1d=session['paydays'][0]['date'],
                           p2a=session['paydays'][1]['amount'], p2d=session['paydays'][1]['date'])


# Route for getting income variable. Stored as session variable.
@app.route('/income', methods=['POST', 'GET'])
def income():
    form = IncomeForm()
    if form.validate_on_submit():
        session['income'] = form.amount.data
        return redirect(url_for('debt'))

    return render_template('income.html', title='Income', form=form)


# Route for adding debt objects. If input validates, a Debt object is created.
# The object is then serialized into json and added to the session.
# The route uses a single submit button. An html button acts as the redirect trigger.
@app.route('/debt', methods=['POST', 'GET'])
def debt():
    form = DebtForm()
    if form.validate_on_submit():
        name = strip_whitespace(form.name.data)
        principal = form.principal.data
        interest = form.interest_rate.data
        minimum = form.minimum.data
        temp = debts.Debt(name, principal, interest, minimum)
        session['debts'] = session_append(session['debts'], to_json(temp))

        return redirect(url_for('debt'))

    return render_template('debt.html', title='Debt', form=form, income=session['income'])


# Route for 'bills route' output. The real logic happens here using the variables assigned to the session before hand.
# See relevant modules for more information.
@app.route('/bill_output')
def bill_output():
    paydays_list = []
    bills_list = []

    for i in session['paydays']:
        paydays_list.append(bills.PayDay.from_json(i))
    for i in session['bills']:
        bills_list.append(bills.Bill.from_json(i))

    print(paydays_list[0].date, '-', paydays_list[1].date)

    enough, leftover, what_do = bills.run(paydays_list, bills_list, paydays_list[0], paydays_list[1])

    return render_template('bill_output.html', title='Bill Output', enough=enough, leftover=leftover, what_do=what_do)


# Route for 'debt route' output. The real logic happens here using the variables assigned to the session before hand.
# See relevant modules for more information.
@app.route('/debt_output')
def debt_output():
    linked_list = debts.LinkedList()
    debts_list = []

    for i in session['debts']:
        debts_list.append(debts.Debt.from_json(i))
    for i in debts_list:
        linked_list.auto_insert(i)

    linked_list.income = session['income']
    linked_list.preserve_payoff_priority()
    payoff_prio = linked_list.pay_off_priority_list

    output = linked_list.run_payoff()
    payoff_month_dict = linked_list.pay_off_month_dictionary

    return render_template('debt_output.html',
                           title='Debt Output',
                           output=output,
                           payoff_prio=payoff_prio,
                           payoff_month_dict=payoff_month_dict)


if __name__ == '__main__':
    app.run(debug=True)
