import re  # import library for regex function


def read_file(filename):  # function that opens and reads a csv file
    with open(filename, "r") as file:
        if file.mode == "r":
            content = file.read()
            data = re.findall(r"(\d{2}\/\d{2}\/\d{4}),([^,]+),([^,]+),([^,]+),([^,]+)\n\b", content)  # regex search
            # that groups data from each column
            return data
            # data[0] = date
            # data[3] = circumstances


def list_all(specificity, data):  # function for listing all names and their net balances
    balances = {}  # creating an empty dictionary
    for row in data:
        amount = row[4]  # assigning variable names that are easy to understand
        to_name = row[2]
        from_name = row[1]
        if from_name in balances:  # if someone has a transaction where they owe money
            balances[from_name] += -float(amount)  # deduct that amount from their balance (square brackets = key)
        else:
            balances[from_name] = -float(amount)  # if there is only one instance of them owing money, their balance
            # is the negative magnitude of that amount
        if to_name in balances:  # if someone has a transaction where they are owed money
            balances[to_name] += float(amount)  # add that amount to their balance
        else:
            balances[to_name] = float(amount)  # if there is only one instance of them being owed money, their balance
            # is that amount
    for person in balances:
        balance = float(format(balances[person], ".2f"))  # formatting currency into floats so arithmetic can be used
        balances[person] = balance  # override the original dict entry with the floats. (Ok because all processing is
        # done)
        if specificity != "y":  # prints a list of all people's names and balances
            if balance < 0:
                print(person + " owes £" + str(abs(balance)))
            else:
                print(person + " is owed £" + str(abs(balance)))
    if specificity == "y":  # used when the user wants a specific person's account balance
        return balances


def list_account(account_name, data):  # function that prints a list of all transactions and net balance for a person
    transaction_dict = {}  # creates an empty dictionary
    counter = 0  # initiates a counter
    for transaction in data:
        if transaction[1] == account_name:  # if someone has a transaction where they are owed money, add to dict
            transaction_dict[counter] = transaction
            counter += 1  # advance counter
        if transaction[2] == account_name:  # if someone has a transaction where they owe money, add to dict
            transaction_dict[counter] = transaction
            counter += 1
    for entry in transaction_dict:
        print(*transaction_dict[entry])  # prints the dictionary of transactions
    balances = list_all("y", data)
    total_balance = balances[account_name]
    if total_balance < 0:
        print("\n" + account_name + " has " + str(counter) + " transactions. In total " + account_name + " owes £" +
              str(abs(total_balance)))
    else:
        print("\n" + account_name + " has " + str(counter) + " transactions. In total " + account_name + " is owed £" +
              str(abs(total_balance)))
    # prints the person's total balance


file_info = read_file(input("Please enter the name of the file you'd like to search (with extension):\n"))  # user
# inputs a file to eb read
print("Please type a command from the following list: \n"
      "List All \nList Account name (e.g. List Account Jon A) \nhelp \nquit")
cont = True  # allows user to exit at some point
while cont:
    command = input()
    if command.lower() == "list all" or command.lower() == "listall":  # user
        # chooses a command
        list_all("n", file_info)
    elif re.search(r"[Ll]ist ?[Aa]ccount", command):  # checks that the user has entered the correct command
        name = re.findall(r"[Ll]ist ?[Aa]ccount ?([A-Z][a-z]* ?[A-Z]?[a-z]*?)\b", command)  # finds name of account
        # they want
        print("Here are the transactions for " + str(name[0]) + ":\n")
        list_account(name[0], file_info)
    elif command == "help":  # help command brings up menu of commands
        print("Please type a command from the following list: \n"
              "List All \nList Account name (e.g. List Account Jon A) \nhelp \nquit")
    elif command == "quit":  # exits the loop
        print("Thanks for visiting!")
        cont = False
        break
    else:
        print("Invalid Command\n")  # if a user enters an invalid command, the loop restarts
        print("Please type a command from the following list: \n"
              "List All \nList Account name (e.g. List Account Jon A) \nhelp \nquit")
