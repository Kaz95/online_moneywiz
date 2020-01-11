import unittest

import app
import bills


# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)


class TestBills(unittest.TestCase):
    def setUp(self):
        self.b1 = bills.Bill("Insurance", 200, 2)
        self.b2 = bills.Bill("Car", 500, 12)
        self.b3 = bills.Bill("House", 700, 28)
        self.json_bill = app.to_json(self.b1)

        self.p1 = bills.PayDay(1000, 5)
        self.p2 = bills.PayDay(500, 25)
        self.json_payday = app.to_json(self.p1)

        self.bills = [self.b1, self.b2, self.b3]
        self.paydays = [self.p1, self.p2]

    def test_add_amounts(self):
        answer1 = bills.Bill.add_amounts(self.bills)
        answer2 = bills.Bill.add_amounts(self.paydays)
        self.assertEqual(answer1, 1400)
        self.assertEqual(answer2, 1500)

    def test_seperate_bills(self):
        a, b = bills.Bill.separate_bills(self.bills, range(5, 20))
        self.assertEqual(a, [self.b2])
        self.assertEqual(b, [self.b1, self.b3])

    def test_payday_from_json(self):
        answer = bills.PayDay.from_json(self.json_payday)
        self.assertEqual(answer.amount, 1000)
        self.assertEqual(answer.date, 5)

    def test_bill_from_json(self):
        answer = bills.Bill.from_json(self.json_bill)
        self.assertEqual(answer.name, 'Insurance')
        self.assertEqual(answer.amount, 200)
        self.assertEqual(answer.date, 2)

    def test_find_first(self):
        first, second = bills.find_first(self.p2, self.p1)
        self.assertEqual(first, self.p1)
        self.assertEqual(second, self.p2)

    def test_run_enough(self):
        enough, leftover, what_do = bills.run(self.paydays, self.bills, self.p1, self.p2)
        self.assertTrue(enough)
        self.assertEqual(leftover, 100)
        self.assertEqual(what_do, 'Save 400 from pp1')

    def test_run_not_enough(self):
        self.bills[0].amount += 200
        enough, leftover, what_do = bills.run(self.paydays, self.bills, self.p1, self.p2)
        self.assertFalse(enough)


if __name__ == '__main__':
    unittest.main()
