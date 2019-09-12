class Transaction():
    def __init__(self, row):
        self.date = row[0]
        self.owed = row[2]
        self.owing = row[1]
        self.reason = row[3]
        self.amount = row[4]

    def get_amount(self):
        return self.amount

    def get_owing(self):
        return self.owing

    def get_owed(self):
        return self.owed


