class Transaction():
    def __init__(self, date, from_person, to_person, narrative, cash_amount):
        self.date = date
        self.owing = from_person
        self.owed = to_person
        self.reason = narrative
        self.amount = cash_amount

    @staticmethod
    def from_csv(csv_row):
        return Transaction(csv_row[0], csv_row[1], csv_row[2], csv_row[3], csv_row[4])

    @staticmethod
    def from_json(json_transaction):
        return Transaction(json_transaction[0], json_transaction[1], json_transaction[2],
                           json_transaction[3], json_transaction[4])

    def get_amount(self):
        return self.amount

    def get_owing(self):
        return self.owing

    def get_owed(self):
        return self.owed
