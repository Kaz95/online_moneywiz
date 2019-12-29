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


if __name__ == '__main__':
    unittest.main()
