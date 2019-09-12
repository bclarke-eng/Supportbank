import logging
import re


class Balances():
    def __init__(self, transactions):
        balances = {}  # creating an empty dictionary
        counter = 1
        for transaction in transactions:
            amount = transaction.get_amount()
            to_name = transaction.get_owed()
            from_name = transaction.get_owing()
            if not re.search(r"\d+\.?\d*", amount):
                logging.info("Invalid entry in Amount field. Invalid entry was: " + amount + ".")
                logging.info("The error was found in transaction number: " + str(counter) + ", and has been skipped.")
                continue
            if from_name in balances:  # if someone has a transaction where they owe money
                balances[from_name] += -float(amount)  # deduct that amount from their balance (square brackets = key)
            else:
                balances[from_name] = -float(amount)  # if there is only one instance of them owing money, their balance
                # is the negative magnitude of that amount
            if to_name in balances:  # if someone has a transaction where they are owed money
                balances[to_name] += float(amount)  # add that amount to their balance
            else:
                balances[to_name] = float(amount)  # if there is only one instance of them being owed money, their
                # balance is that amount
            counter += 1
        self.balances = balances

    def display(self):
        for account in self.balances:
            balance = float(format(self.balances[account], ".2f"))
            if balance < 0:
                print(account + " owes £" + str(abs(balance)))
            else:
                print(account + " is owed £" + str(balance))

    def get(self, name):
        return self.balances[name]

    def individual_display(self, fullname):
        for name in self.balances:
            balance = float(format(self.balances[name], ".2f"))
            if self.balances[fullname] == self.balances[name]:
                if balance < 0:
                    print(name + " owes £" + str(abs(balance)))
                else:
                    print(name + " is owed £" + str(balance))
