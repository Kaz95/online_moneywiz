from flask import Flask, render_template, redirect, url_for, session
from forms import BillForm, PaydayForm, IncomeForm, DebtForm
import bills

app = Flask(__name__)
app.config['FLASK_DEBUG'] = True
app.config['SECRET_KEY'] = '3'


@app.route('/')
@app.route('/home')
def home():
    session.clear()
    session['bills'] = []
    # session['paydays'] = []

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
            temp_list = session['paydays']
            temp_list.append(temp.to_json())
            session['paydays'] = temp_list
            print(session)
            print(session['paydays'])
            return redirect(url_for('payday'))
        else:
            # session['hokay'] = 'gofuckflask'
            temp_list = session['paydays']
            temp_list.append(temp.to_json())
            session['paydays'] = temp_list
            print('p1 exists; now p2 does as well')
            print(session)
            print(session['paydays'])
            return redirect(url_for('bill'))
        # return redirect(url_for('bill', a=amount, d=date))
    return render_template('payday.html', title='Payday', form=form)


@app.route('/bill', methods=['POST', 'GET'])
def bill():
    form = BillForm()
    if form.validate_on_submit():
        name = form.name.data
        amount = form.amount.data
        date = form.date.data
        temp = bills.Bill(name, amount, date)
        some_bill = session[temp.name] = temp.to_json()
        session['bills'].append(some_bill)
        print(session['bills'])

        if form.add_bill.data is True:
            return redirect(url_for('bill'))
        elif form.done.data is True:
            return redirect(url_for('bill_output'))

    # amount = request.args.get('a')
    # date = request.args.get('d')
    # return render_template('bill.html', title='Bill', form=form)
    # return render_template('bill.html', title='Bill', form=form, a=amount, d=date)
    return render_template('bill.html', title='bill', form=form,
                           p1a=session['paydays'][0]['amount'], p1d=session['paydays'][0]['date'],
                           p2a=session['paydays'][1]['amount'], p2d=session['paydays'][1]['date'])


@app.route('/income')
def income():
    form = IncomeForm()
    return render_template('income.html', title='Income', form=form)


@app.route('/debt')
def debt():
    form = DebtForm()
    return render_template('debt.html', title='Debt', form=form)


@app.route('/bill_output')
def bill_output():
    paydays_list = []
    bills_list = []
    for i in session['paydays']:
        paydays_list.append(bills.PayDay.from_json(i))
    for i in session['bills']:
        bills_list.append(bills.Bill.from_json(i))

    some_string, some_dict, enough, leftover = bills.run(paydays_list, bills_list, paydays_list[0], paydays_list[1])
    return render_template('bill_output.html', title='Bill Output', enough=enough, leftover=leftover)


@app.route('/debt_output')
def debt_output():
    return render_template('debt_output.html', title='Debt Output')


if __name__ == '__main__':
    app.run(debug=True)
