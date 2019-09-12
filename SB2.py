import re  # import library for regex function
import logging  # import library for logging
from Balances import Balances
from Transaction import Transaction

logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)


def read_file(filename):  # function that opens and reads a csv file
    with open(filename, "r") as file:
        if file.mode == "r":
            content = file.read()
            logging.info('Program initialised. User entered a valid file.')  # creates a log
            logging.info(filename + " has been opened in read mode.")
            rows = re.findall(r"(\d{2}\/\d{2}\/\d{4}),([^,]+),([^,]+),([^,]+),([^,]+)\n\b", content)  # regex search
            # that groups data from each column

            transactions = []
            for row in rows:
                transactions.append(Transaction(row))

            logging.info(filename + " has been read and closed.")
            return transactions
            # data[0] = date
            # data[3] = circumstances


def list_all(balances):  # function for listing all names and their net balances
    logging.info("List All function complete.")
    balances.display()

    return balances


def filter_transactions(account_name, transactions):
    logging.info("User selected List Account function for " + account_name)
    transaction_dict = {}  # creates an empty dictionary
    counter = 0  # initiates a counter
    for transaction in transactions:
        if transaction.owing == account_name:  # if someone has a transaction where they are owed money, add to dict
            transaction_dict[counter] = transaction
            counter += 1  # advance counter
            print(transaction.date, transaction.owed, transaction.owing,
                  "£" + format(float(transaction.amount), ".2f"))  # prints the transactions
        if transaction.owed == account_name:  # if someone has a transaction where they owe money, add to dict
            transaction_dict[counter] = transaction
            counter += 1
            print(transaction.date, transaction.owed, transaction.owing,
                  "£" + format(float(transaction.amount), ".2f"))  # prints the transactions
    logging.info(account_name + "'s account contained " + str(counter) + " transactions")


def list_account(account_name, transactions):  # function that prints a list of all transactions and net balance for a
    # person
    filter_transactions(account_name, transactions)

    logging.info("Total balance for " + account_name + " is being calculated.")
    balances.individual_display(account_name)
    logging.info("List account function was completed for " + account_name)


logging.info("User was asked to input a file name.")
transactions = []
balances = []
cont = True
while cont:
    file_input = input("Please enter the name of the file you'd like to search (with extension):\n")
    try:
        transactions = read_file(file_input)  # user inputs a file to be read
        balances = Balances(transactions)
        cont = False
        # do something
    except FileNotFoundError:
        logging.info("The user entered an invalid file name. User entered: " + file_input)
        print("Sorry. That file name is invalid.")

logging.info("User was asked to select a command.")
print("Please type a command from the following list: \n"
      "List All \nList Account name (e.g. List Account Jon A) \nhelp \nquit")

cont = True  # allows user to exit at some point
while cont:
    command = input()
    if command.lower() == "list all" or command.lower() == "listall":  # user
        # chooses a command
        logging.info("User selected the List All function.")
        list_all(balances)
        logging.info("User was asked to select a command.")
        print("Please type a command from the following list: \n"
              "List All \nList Account name (e.g. List Account Jon A) \nhelp \nquit")
    elif re.search(r"[Ll]ist ?[Aa]ccount", command):  # checks that the user has entered the correct command
        name = re.findall(r"[Ll]ist ?[Aa]ccount ?([A-Z][a-z]* ?[A-Z]?[a-z]*?)\b", command)[0]  # finds name of account
        # they want
        print("Here are the transactions for " + name + ":\n")
        list_account(name, transactions)
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
            "User entered an invalid command and was asked to try again.  The command entered was: " + command)
        logging.info("User was asked to select a command.")
