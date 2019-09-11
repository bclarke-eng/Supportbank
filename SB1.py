import csv

with open("Transactions2014.csv", "r") as file:
    readfile = csv.reader(file, delimiter=",")  # reads the csv file
    next(readfile, None)  # skips column headers

    From = []
    To = []
    Narrative = []
    Amount = []

    for row in readfile:
        owing = row[1]
        owed = row[2]
        narr = row[3]
        money = row[4]

        From.append(owing)
        To.append(owed)
        Narrative.append(narr)
        Amount.append(float(money))  # stores currency as a float to allow for addition

    print(Amount)
