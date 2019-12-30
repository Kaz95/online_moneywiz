# Handles all bill related backend


class PayDay:
    def __init__(self, amount, date):
        self.amount = amount
        self.date = date

    def to_json(self):
        return self.__dict__

    # Creates and returns a PayDay object from json(dictionary)
    @staticmethod
    def from_json(some_json):
        temp = PayDay(some_json['amount'], some_json['date'])
        return temp

    # Returns the sum of a list of objects by accessing their amount attribute.
    @staticmethod
    def add_amounts(some_list):
        total = 0

        for obj in some_list:
            total += obj.amount

        return total


class Bill(PayDay):
    def __init__(self, name, amount, date):
        PayDay.__init__(self, amount, date)
        self.name = name

    # Creates and returns a Bill object from json(dictionary)
    @staticmethod
    def from_json(some_json):
        temp = Bill(some_json['name'], some_json['amount'], some_json['date'])
        return temp

    # Separates a list of Bill objects into one of two lists, based on a given range.
    @staticmethod
    def separate_bills(list_of_bills, middle_range):
        pp1 = []
        pp2 = []
        for bill in list_of_bills:
            if bill.date in middle_range:
                pp1.append(bill)
            else:
                pp2.append(bill)

        return pp1, pp2


# Main bills function. Returns an pre-formatted output string.
def run(payday_list, bills_list, payday1, payday2):
    # Find totals of each list of objects
    paydays_sum = PayDay.add_amounts(payday_list)
    bills_sum = Bill.add_amounts(bills_list)

    # Leftover will be the value passed to debts.py
    left_over = paydays_sum - bills_sum

    # Decide if there is enough money overall

    # Changing output_dictionary to False signifies not having enough money.
    if left_over < 0:
        print("You don't have enough money!")
        enough = False

    # If leftover is greater than 0 assign it as a value of its respective key.
    else:
        enough = True
        print("You have enough money!")
        print(f"You have {left_over} left over")

        # Figure out which payday comes first in the month
        first_payday = min(payday1.date, payday2.date)
        second_payday = max(payday1.date, payday2.date)

        # Middle range will be the days covered by the first payday
        # All other days not in this range will be covered bt the second payday
        middle_range = range(first_payday, second_payday)
        # Separate the bills into two lists, each representing a given pay period
        first_pay_period, second_pay_period = Bill.separate_bills(bills_list, middle_range)

        # Total the amount of the bills for each pay period
        pp1sum = Bill.add_amounts(first_pay_period)
        pp2sum = Bill.add_amounts(second_pay_period)

        # Logic that determines which pay period has a surplus, or if both do.
        if payday1.amount > pp1sum and payday2.amount > pp2sum:
            print("I'm rich bitch!")
        elif payday1.amount < pp1sum:
            print(f"Save {pp1sum - payday1.amount} from pp2")
        else:
            print(f"Save {pp2sum - payday2.amount} from pp1")

    return enough, left_over
