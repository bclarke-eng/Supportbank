import re  # import library for regex function
import logging  # import library for logging

logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)


def read_file(filename):  # function that opens and reads a csv file
    with open(filename, "r") as file:
        if file.mode == "r":
            content = file.read()
            logging.info('Program initialised. User entered a valid file.')  # creates a log
            logging.info(str(filename) + " has been opened in read mode.")
            data = re.findall(r"(\d{2}\/\d{2}\/\d{4}),([^,]+),([^,]+),([^,]+),([^,]+)\n\b", content)  # regex search
            # that groups data from each column
            logging.info(str(filename) + " has been read and closed.")
            return data
            # data[0] = date
            # data[3] = circumstances


def list_all(specificity, data):  # function for listing all names and their net balances
    balances = {}  # creating an empty dictionary
    counter = 1
    for row in data:
        amount = row[4]  # assigning variable names that are easy to understand
        if not re.search(r"\d+\.?\d*", amount):
            logging.info("Invalid entry in Amount field. Invalid entry was: " + str(amount) + ".")
            logging.info("The error was found in transaction number: " + str(counter) + ", and has been skipped.")
            continue
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
        counter += 1
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
    logging.info("List All function complete.")


def list_account(account_name, data):  # function that prints a list of all transactions and net balance for a person
    logging.info("User selected List Account function for " + str(account_name))
    transaction_dict = {}  # creates an empty dictionary
    counter = 0  # initiates a counter
    for transaction in data:
        if transaction[1] == account_name:  # if someone has a transaction where they are owed money, add to dict
            transaction_dict[counter] = transaction
            counter += 1  # advance counter
        if transaction[2] == account_name:  # if someone has a transaction where they owe money, add to dict
            transaction_dict[counter] = transaction
            counter += 1
    logging.info(str(account_name) + "'s account contained " + str(counter) + " transactions")
    for entry in transaction_dict:
        print(*transaction_dict[entry])  # prints the dictionary of transactions
    logging.info("Total balance for " + str(account_name) + " is being calculated.")
    balances = list_all("y", data)
    total_balance = balances[account_name]
    if total_balance < 0:
        print("\n" + account_name + " has " + str(counter) + " transactions. In total " + account_name + " owes £" +
              str(abs(total_balance)))
    else:
        print("\n" + account_name + " has " + str(counter) + " transactions. In total " + account_name + " is owed £" +
              str(abs(total_balance)))
    # prints the person's total balance
    logging.info("List account function was completed for " + str(account_name))


logging.info("User was asked to input a file name.")
while True:
    file_input = input("Please enter the name of the file you'd like to search (with extension):\n")
    try:
        file_info = read_file(file_input)  # user inputs a file to be read
    except FileNotFoundError:
        logging.info("The user entered an invalid file name. User entered: " + str(file_input))
        print("Sorry. That file name is invalid.")
        continue
    else:
        break

logging.info("User was asked to select a command.")
print("Please type a command from the following list: \n"
      "List All \nList Account name (e.g. List Account Jon A) \nhelp \nquit")

cont = True  # allows user to exit at some point
while cont:
    command = input()
    if command.lower() == "list all" or command.lower() == "listall":  # user
        # chooses a command
        logging.info("User selected the List All function.")
        list_all("n", file_info)
        logging.info("User was asked to select a command.")
        print("Please type a command from the following list: \n"
              "List All \nList Account name (e.g. List Account Jon A) \nhelp \nquit")
    elif re.search(r"[Ll]ist ?[Aa]ccount", command):  # checks that the user has entered the correct command
        name = re.findall(r"[Ll]ist ?[Aa]ccount ?([A-Z][a-z]* ?[A-Z]?[a-z]*?)\b", command)  # finds name of account
        # they want
        print("Here are the transactions for " + str(name[0]) + ":\n")
        list_account(name[0], file_info)
        logging.info("User was asked to select a command.")
        print("Please type a command from the following list: \n"
              "List All \nList Account name (e.g. List Account Jon A) \nhelp \nquit")
    elif command == "help":  # help command brings up menu of commands
        print("Please type a command from the following list: \n"
              "List All \nList Account name (e.g. List Account Jon A) \nhelp \nquit")
        logging.info("User requested help. Help menu displayed.")
        logging.info("User was asked to select a command.")
    elif command == "quit":  # exits the loop
        print("Thanks for visiting!")
        logging.info("User quit the program.")
        cont = False
        logging.info("Program terminated.")
        break
    else:
        print("Invalid Command\n")  # if a user enters an invalid command, the loop restarts
        print("Please type a command from the following list: \n"
              "List All \nList Account name (e.g. List Account Jon A) \nhelp \nquit")
        logging.info(
            "User entered an invalid command and was asked to try again.  The command entered was: " + str(command))
        logging.info("User was asked to select a command.")
