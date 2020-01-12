import unittest
import debts


# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)

class TestDebt(unittest.TestCase):
    def setUp(self):
        # Test debts
        self.d1 = debts.Debt("credit card", 40, .04, 10)
        self.d2 = debts.Debt("loan", 60, .03, 10)
        self.d3 = debts.Debt("car", 20, .02, 10)
        self.d4 = debts.Debt("Something", 100, .01, 10)

        self.d5 = debts.Debt("To be inserted", 150, 0, 10)

        self.linked_list = debts.LinkedList()
        self.linked_list.income = 50
        self.linked_list.auto_insert(self.d1)
        self.linked_list.auto_insert(self.d2)
        self.linked_list.auto_insert(self.d3)
        self.linked_list.auto_insert(self.d4)

        self.json_debt = {'name': 'Ima Json Debt', 'principal': 123, 'interest': 4, 'minimum': 10}

    def test_move_cursors(self):
        cur = self.linked_list.head
        cur, prev = debts.LinkedList.move_cursors(cur)
        self.assertEqual(cur, self.linked_list.head.next, "cur pointer did not move correctly")
        self.assertEqual(prev, self.linked_list.head, "prev pointer did not move correctly")

    def test_insert(self):
        prev = self.linked_list.head
        cur = prev.next

        node = debts.Node(self.d5)
        debts.LinkedList.manual_insertion(node, cur, prev)

        self.assertEqual(prev.next, node, "Node not in correct position")
        self.assertEqual(node.next, cur, "Cur not in correct position")

    def test_find_spillover(self):
        principal = -100
        spillover = debts.LinkedList.find_spillover(principal)
        self.assertEqual(spillover, 100)

    def test_prime_cursors(self):
        cur, prev = self.linked_list.prime_cursors()
        self.assertEqual(cur, self.linked_list.head)
        self.assertEqual(prev, None)

    def test_insert_new_head(self):
        self.linked_list.insert_new_head(self.d5)
        self.assertEqual(self.linked_list.head, self.d5)

    def test_prepare_recalc(self):
        self.linked_list.head.data.interest_incurred = 10
        spillover = 5
        self.linked_list.prepare_recalc(spillover)
        self.assertEqual(self.linked_list.head.data.principal, 25)

    def test_recalc_interst(self):
        cur = self.linked_list.head.next
        self.linked_list.generate_interest(cur)
        self.assertEqual(round(cur.data.interest_incurred, 2), 1.8, "Wrong interest calculated")
        self.assertEqual(cur.data.principal, 61.8, "Wrong principal")

        self.linked_list.generate_interest()
        self.assertEqual(self.linked_list.head.data.interest_incurred, 1.6, "Wrong interest calculated")
        self.assertEqual(self.linked_list.head.data.principal, 41.6, "Wrong principal")

    def test_add_to_leftover(self):
        cur = self.linked_list.head
        self.linked_list.add_to_leftover(cur)
        self.assertEqual(self.linked_list.leftover, 10)

    def test_spill(self):
        self.linked_list.head.data.principal = -10
        self.linked_list.spill()

        self.assertEqual(self.linked_list.head.data.name, "loan")
        self.assertEqual(self.linked_list.head.data.principal, 50, "single spill case failed")

    def test_multiple_spill(self):
        self.linked_list.head.data.principal = -100
        self.linked_list.spill()

        self.assertEqual(self.linked_list.head.data.name, "Something")
        self.assertEqual(self.linked_list.head.data.principal, 80)

    def test_preserve_payoff_priority(self):
        self.linked_list.preserve_payoff_priority()
        print(self.linked_list.pay_off_priority_list)
        self.assertEqual(self.linked_list.pay_off_priority_list[0].data, self.d1)
        self.assertEqual(self.linked_list.pay_off_priority_list[1].data, self.d2)
        self.assertEqual(self.linked_list.pay_off_priority_list[2].data, self.d3)
        self.assertEqual(self.linked_list.pay_off_priority_list[3].data, self.d4)



    def test_debt_from_json(self):
        answer = debts.Debt.from_json(self.json_debt)
        self.assertEqual(answer.name, 'Ima Json Debt')
        self.assertEqual(answer.principal, 123)
        self.assertEqual(answer.interest, 4)
        self.assertEqual(answer.minimum, 10)

    # This not slinging an error is the test.
    def test_run_payoff(self):
        self.linked_list.run_payoff()

    def test_run_payoff_cant_afford_minimums(self):
        self.unaffordable_debt = debts.Debt('Foo', 1000, 100, 9999)
        self.linked_list.auto_insert(self.unaffordable_debt)
        answer = self.linked_list.run_payoff()
        self.assertEqual(answer, "You don't have enough to cover minimums, refinance.")

    def test_run_payoff_need_refinance(self):
        self.unaffordable_debt = debts.Debt('Foo', 1000, 100, 10)
        self.linked_list.auto_insert(self.unaffordable_debt)
        answer = self.linked_list.run_payoff()
        self.assertEqual(answer, "Refinance, a debts interest is too high.")


class TestAutoInsertEdgeCases(unittest.TestCase):
    def setUp(self):
        self.d1 = debts.Debt('Ima Debt', 123, 5, 10)
        self.linked_list = debts.LinkedList()
        self.linked_list.auto_insert(self.d1)

    def test_greater_interest_and_new_head(self):
        self.d2 = debts.Debt('Ima Another Debt', 123, 10, 10)
        self.linked_list.auto_insert(self.d2)
        self.assertEqual(self.linked_list.head.data, self.d2)

    def test_greater_interest(self):
        self.d2 = debts.Debt('Ima Another Debt', 123, 10, 10)
        self.linked_list.auto_insert(self.d2)
        self.d3 = debts.Debt('Foo', 123, 7, 10)
        self.linked_list.auto_insert(self.d3)


class TestGenerateInterestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.linked_list = debts.LinkedList()
        self.unpayable_debt = debts.Debt('Foo', 1000, 1000, 10)
        self.linked_list.head = debts.Node(self.unpayable_debt)

    def test_generate_interest_edge(self):
        cur = self.linked_list.head
        answer = self.linked_list.generate_interest(cur)
        answer2 = self.linked_list.generate_interest()
        self.assertTrue(answer)
        self.assertTrue(answer2)


if __name__ == '__main__':
    unittest.main()
