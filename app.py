from flask import Flask, render_template, redirect, url_for, session, request, flash
from forms import BillForm, PaydayForm, IncomeForm, DebtForm
import bills
import debts

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'


def session_append(session_list, apendee):
    temp = session_list
    temp.append(apendee)
    return temp


def strip_whitespace(some_string):
    return " ".join(some_string.split())


@app.route('/')
@app.route('/home')
def home():
    session.clear()
    session['bills'] = []
    # session['paydays'] = []
    session['debts'] = []

    return render_template('home.html')


@app.route('/payday', methods=['POST', 'GET'])
def payday():
    form = PaydayForm()
    if form.validate_on_submit():
        amount = form.amount.data
        date = form.date.data
        temp = bills.PayDay(amount, date)
        print(session)

        if 'paydays' not in session:
            print('p1 did not exist; now does')
            session['paydays'] = []
            session['paydays'] = session_append(session['paydays'], temp.to_json())
            print(session)
            print(session['paydays'])
            return redirect(url_for('payday'))
        else:
            # session['hokay'] = 'gofuckflask'
            session['paydays'] = session_append(session['paydays'], temp.to_json())
            print('p1 exists; now p2 does as well')
            print(session)
            print(session['paydays'])
            return redirect(url_for('bill'))
    # else:
    #     if form.amount.errors:
    #         for error in form.amount.errors:
    #             flash(error)
    #     if form.date.errors:
    #         for error in form.date.errors:
    #             flash(error)
        # return redirect(url_for('bill', a=amount, d=date))
    return render_template('payday.html', title='Payday', form=form)


@app.route('/bill', methods=['POST', 'GET'])
def bill():
    form = BillForm()
    if request.method == 'POST':
        if form.done.data is True:
            return redirect(url_for('bill_output'))
    if form.validate_on_submit():
        name = form.name.data
        amount = form.amount.data
        date = form.date.data
        temp = bills.Bill(name, amount, date)
        session['bills'] = session_append(session['bills'], temp.to_json())
        print(session)
        print(session['bills'])

        return redirect(url_for('bill'))

        # if form.add_bill.data is True:
        #     return redirect(url_for('bill'))
        # elif form.done.data is True:
        #     return redirect(url_for('bill_output'))

    # amount = request.args.get('a')
    # date = request.args.get('d')
    # return render_template('bill.html', title='Bill', form=form, a=amount, d=date)
    return render_template('bill.html', title='bill', form=form,
                           p1a=session['paydays'][0]['amount'], p1d=session['paydays'][0]['date'],
                           p2a=session['paydays'][1]['amount'], p2d=session['paydays'][1]['date'])


@app.route('/income', methods=['POST', 'GET'])
def income():
    form = IncomeForm()
    if form.validate_on_submit():
        session['income'] = form.amount.data
        return redirect(url_for('debt'))

    return render_template('income.html', title='Income', form=form)


@app.route('/debt', methods=['POST', 'GET'])
def debt():
    form = DebtForm()
    if form.validate_on_submit():
        name = form.name.data
        principal = form.principal.data
        interest = form.interest_rate.data
        minimum = form.minimum.data
        temp = debts.Debt(name, principal, interest, minimum)
        session['debts'] = session_append(session['debts'], temp.to_json())
        return redirect(url_for('debt'))

    return render_template('debt.html', title='Debt', form=form, income=session['income'])


@app.route('/bill_output')
def bill_output():

    paydays_list = []
    bills_list = []

    for i in session['paydays']:
        paydays_list.append(bills.PayDay.from_json(i))
    for i in session['bills']:
        bills_list.append(bills.Bill.from_json(i))

    print(type(bills_list[0].amount))
    print(type(bills_list[0].date))
    print(type(paydays_list[0].amount))
    print(type(paydays_list[0].date))

    some_string, some_dict, enough, leftover = bills.run(paydays_list, bills_list, paydays_list[0], paydays_list[1])

    return render_template('bill_output.html', title='Bill Output', enough=enough, leftover=leftover)


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
    payoff_month_dict = linked_list.pay_off_month_dictionary

    output = linked_list.run_payoff()

    return render_template('debt_output.html',
                           title='Debt Output',
                           output=output,
                           payoff_prio=payoff_prio,
                           payoff_month_dict=payoff_month_dict)


if __name__ == '__main__':
    app.run(debug=True)
