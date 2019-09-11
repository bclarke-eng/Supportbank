import re


def read_file(filename):
    with open("Transactions2014.csv", "r") as file:
        if file.mode == "r":
            content = file.read()
            # data = re.findall(r"\d{2}\/\d{2}\/\d{4},([^,]+),([^,]+),[^,]+,([^,]+)\n\b", content)
            data = re.findall(r"(\d{2}\/\d{2}\/\d{4}),([^,]+),([^,]+),([^,]+),([^,]+)\n\b", content)
            return data
            # data[0] = date
            # data[1] = from
            # data[2] = to
            # data[3] = circumstances
            # data[4] = amount


def list_all(specificity, data):
    balances = {}
    for row in data:
        amount = row[4]
        to_name = row[2]
        from_name = row[1]
        if from_name in balances:
            balances[from_name] += -float(amount)
        else:
            balances[from_name] = -float(amount)
        if to_name in balances:
            balances[to_name] += float(amount)
        else:
            balances[to_name] = float(amount)
    for person in balances:
        balance = float(format(balances[person], ".2f"))
        balances[person] = balance
        if specificity != "y":
            print(person + " : £" + str(balance))
    if specificity == "y":
        return balances


def list_account(account_name, data):
    transaction_dict = {}
    counter = 0
    for transaction in data:
        if transaction[1] == account_name:
            transaction_dict[counter] = transaction
            counter += 1
        if transaction[2] == account_name:
            transaction_dict[counter] = transaction
            counter += 1
    for entry in transaction_dict:
        print(*transaction_dict[entry])
    balances = list_all("y", data)
    total_balance = balances[account_name]
    print("\n" + account_name + " has " + str(counter) + " transactions. Total balance: £" + str(total_balance))


file_info = read_file("Transactions2014.csv")
print("Please type a command from the following list: \n"
      "List All \nList Account name (e.g. List Account Jon A) \nhelp \nquit")
cont = True
while cont:
    command = input()
    if command == "List All" or command == "list all" or command == "listall" or command == "ListAll":
        list_all("n", file_info)
    elif re.search(r"[Ll]ist ?[Aa]ccount", command):
        name = re.findall(r"[Ll]ist ?[Aa]ccount ?([A-Z][a-z]* ?[A-Z]?[a-z]*?)\b", command)
        print("Here are the transactions for " + str(name[0]) + ":\n")
        list_account(name[0], file_info)
    elif command == "help":
        print("Please type a command from the following list: \n"
              "List All \nList Account name (e.g. List Account Jon A) \nhelp \nquit")
    elif command == "quit":
        print("Thanks for visiting!")
        cont = False
        break
    else:
        print("Invalid Command\n")
        print("Please type a command from the following list: \n"
              "List All \nList Account name (e.g. List Account Jon A) \nhelp \nquit")