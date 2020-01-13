import unittest

import routes
import bills
import debts


# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)


class TestApp(unittest.TestCase):
    def setUp(self):
        self.bill = bills.Bill('Bill Name', 123, 1)
        self.bill = routes.to_json(self.bill)

        self.debt = debts.Debt('Debt Name', 123, 4, 10)
        self.debt = routes.to_json(self.debt)

        self.apendee_bill = bills.Bill('Bill Apendee', 123, 1)
        self.apendee_debt = debts.Debt('Debt Apendee', 123, 4, 10)

        self.white_space_bill = bills.Bill('  Bill  with     space  ', 123, 1)
        self.white_space_debt = debts.Debt('  Debt  with     space  ', 123, 4, 10)

        self.session = {'bills': [self.bill], 'debts': [self.debt]}

    def test_duplicate_name(self):
        unexpected = 'Clown'
        expected_bill = 'Bill Name'
        expected_debt = 'Debt Name'

        answer = routes.duplicate_name(unexpected, self.session['bills'])
        answer1 = routes.duplicate_name(expected_bill, self.session['bills'])
        answer2 = routes.duplicate_name(expected_debt, self.session['debts'])

        self.assertFalse(answer)
        self.assertTrue(answer1)
        self.assertTrue(answer2)

    def test_session_append(self):
        json_apendee_bill = routes.to_json(self.apendee_bill)
        json_apendee_debt = routes.to_json(self.apendee_debt)

        routes.session_append(self.session['bills'], json_apendee_bill)
        routes.session_append(self.session['debts'], json_apendee_debt)

        self.assertIn(json_apendee_bill, self.session['bills'])
        self.assertIn(json_apendee_debt, self.session['debts'])

    def test_strip_whitespace(self):
        bill_answer = routes.strip_whitespace(self.white_space_bill.name)
        debt_answer = routes.strip_whitespace(self.white_space_debt.name)
        self.assertEqual(bill_answer, 'Bill with space')
        self.assertEqual(debt_answer, 'Debt with space')


if __name__ == '__main__':
    unittest.main()
