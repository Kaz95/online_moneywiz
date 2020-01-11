# Handles all debt related backend


class Debt:
    def __init__(self, name, principal, interest, minimum):
        self.name = name
        self.principal = principal
        self.interest = interest
        self.minimum = minimum

        self.interest_incurred = 0

    # TODO: Test
    # Creates and returns a Debt object from json(dictionary). Converts whole number percent to decimal.
    @staticmethod
    def from_json(some_json):
        whole_num_interest = some_json['interest']
        # percent_interest = whole_num_interest / 100
        debt = Debt(some_json['name'], some_json['principal'], whole_num_interest, some_json['minimum'])
        return debt

# Test debts
# d1 = Debt("credit card", 40, .04, 10)
# d2 = Debt("loan", 60, .03, 10)
# d3 = Debt("car", 20, .02, 10)
# d4 = Debt("Something", 100, .01, 10)


# Helper class for linked list.
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# TODO: Look this over for fat.
# TODO: Consider renaming income to leftover; everywhere.
# Purpose modified linked list class definition
class LinkedList:

    def __init__(self):
        self.head = None
        self.income = 0  # The value that will eventually be passed from bills.py
        self.minimums = 0  # Total minimum payment of all debts. Used to calculate if enough money for minimums.
        self.leftover = 0   # L = (Income - minimums)
        self.temp_leftover = 0  # Used to hold leftover during actual iteration. Refilled at the start of each pass.
        self.months_to_payoff = 0   # += 1 once per full pass of linked list

        # Used to keep track of which debts have been paid during a given pass.
        # Needed to decide if interest needs recalculating
        self.interest_already_paid_list = []

        self.pay_off_priority_list = []  # Used to preserve payoff priority for final debt output string
        self.pay_off_month_dictionary = {}  # Used to capture pay off month of each debt for output string

        self.need_refinance = None

    # Prepare cursors for list traversal
    # Start from head
    def prime_cursors(self):
        cur = self.head
        prev = None
        return cur, prev

    @staticmethod
    def move_cursors(cur):
        prev = cur
        cur = cur.next
        return cur, prev

    # Insert new head node
    def insert_new_head(self, node):
        temp = self.head
        self.head = node
        self.head.next = temp

    @staticmethod
    def manual_insertion(node, cur, prev):
        prev.next = node
        prev.next.next = cur

    # TODO: Test; Create a scenario where all lines are hit. Redo Coverage if needed.
    # Fills linked list with debt object
    # Sorts objects into the list based on interest rate
    # Keeps running tally of minimums
    def auto_insert(self, some_debt):
        self.minimums += some_debt.minimum
        node = Node(some_debt)

        if self.head is None:
            self.head = node
        else:
            cur, prev = self.prime_cursors()
            while cur is not None:
                if node.data.interest <= cur.data.interest:
                    cur, prev = LinkedList.move_cursors(cur)
                elif prev is None:
                    self.insert_new_head(node)
                    break
                else:
                    LinkedList.manual_insertion(node, cur, prev)
                    break

            if cur is None:
                if node.data.interest <= prev.data.interest:
                    prev.next = node
                else:
                    self.insert_new_head(node)

    @staticmethod
    def find_spillover(principal):
        spillover = 0 - principal
        return spillover

    # Remove previously incurred interest in preparation for interest recalculation
    # Used when payment spills over into new node
    def prepare_recalc(self, spillover):
        self.head.data.principal -= self.head.data.interest_incurred
        self.head.data.principal -= spillover
        print(self.head.data.name, round(self.head.data.principal, 2))

    # TODO: Test; While most of the lines are being hit, core functionality is not being tested for proper return value.
    # Single function that calculates and incurs interest
    # Generates interest on head node by default unless a node is passes as param
    def generate_interest(self, cur=None):
        if cur:
            cur.data.interest_incurred = cur.data.principal * cur.data.interest
            if cur.data.interest_incurred > self.income:
                return True
            cur.data.principal += cur.data.interest_incurred
        else:
            self.head.data.interest_incurred = self.head.data.principal * self.head.data.interest
            if self.head.data.interest_incurred > self.income:
                return True
            self.head.data.principal += self.head.data.interest_incurred
            print(self.head.data.name, round(self.head.data.principal, 2))

    # Used to increased leftover amount after a give cursor is paid off.
    def add_to_leftover(self, cur):
        self.leftover += cur.data.minimum

    # Currently used to visually ensure list has been sorted correctly.
    def print_list(self):
        cur = self.head
        while cur:
            print(cur.data.name)
            cur = cur.next

    # Recursive function to handle spillover from paid off head node.
    def spill(self):
        if self.head.data.principal <= 0:
            spillover = LinkedList.find_spillover(self.head.data.principal)
            self.head = self.head.next
            if self.head:
                self.head.data.principal -= spillover
                print(self.head.data.name, round(self.head.data.principal, 2))
                self.spill()

    # TODO: Unittest
    # Recursive function to handle spillover from paid off cursor node.
    def special_spill_not_head(self, cur, prev):
        if cur.data.principal <= 0:
            spillover = LinkedList.find_spillover(cur.data.principal)
            prev.next = cur.next
            if self.head:
                self.prepare_recalc(spillover)

                if self.head.data.principal <= 0:
                    self.special_spill()
                else:
                    self.generate_interest()

    # TODO: Unittest
    # Handles a cursor node being paid off, and its spill over paying off the head node.
    # Only used within special_spill_not_head()
    def special_spill(self):
        if self.head.data.principal <= 0:
            spillover = LinkedList.find_spillover(self.head.data.principal)
            self.head = self.head.next
            if self.head:
                if self.head in self.interest_already_paid_list:
                    self.prepare_recalc(spillover)
                    if self.head.data.principal <= 0:
                        self.special_spill()
                    else:
                        self.generate_interest()
                else:
                    self.head.data.principal -= spillover
                    self.special_spill()

    # TODO: Test; Whole thing, then go back and write tests for lines that weren't hit.
    # Meat and potatoes function.
    # Iterates through linked list paying down principles and removing paid off nodes.
    # Keeps tracks of number of passes(months)
    # Leverages the spill() functions to handle spillover of paid debts.
    # Returns number of months till all debts are paid based on available information.
    def run_payoff(self):
        print(f"Minimums: {self.minimums}")

        if self.minimums > self.income:
            return "You don't have enough to cover minimums, refinance."

        self.leftover = self.income - self.minimums

        while self.head:
            cur, prev = self.prime_cursors()
            self.temp_leftover += self.leftover

            while cur:
                if cur == self.head:
                    cur.data.principal -= (cur.data.minimum + self.temp_leftover)
                    self.temp_leftover = 0

                    if cur.data.principal <= 0:
                        self.add_to_leftover(cur)
                        self.spill()
                        print(cur.data.name, f"paid off in {self.months_to_payoff + 1} months(s)")
                        self.pay_off_month_dictionary[cur.data.name] = self.months_to_payoff + 1
                    else:
                        self.need_refinance = self.generate_interest(cur)
                        print(cur.data.name, round(cur.data.principal, 2))
                        self.interest_already_paid_list.append(cur)
                else:
                    cur.data.principal -= cur.data.minimum

                    if cur.data.principal <= 0:
                        print(cur.data.name, f"paid off in {self.months_to_payoff + 1} months(s)")
                        self.pay_off_month_dictionary[cur.data.name] = self.months_to_payoff + 1
                        self.add_to_leftover(cur)
                        self.special_spill_not_head(cur, prev)
                    else:
                        self.need_refinance = self.generate_interest(cur)
                        print(cur.data.name, round(cur.data.principal, 2))
                        self.interest_already_paid_list.append(cur)

                if self.need_refinance is True:
                    self.head = None
                    break
                cur, prev = LinkedList.move_cursors(cur)

            self.months_to_payoff += 1

        if self.need_refinance is True:
            return "Refinance, a debts interest is too high."

        print(self.pay_off_month_dictionary)

    # TODO: Test
    # Traverse list and append each node to a list
    def preserve_payoff_priority(self):
        cur = self.head
        while cur:
            self.pay_off_priority_list.append(cur)
            cur = cur.next
