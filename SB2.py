import re  # import library for regex function
import logging  # import library for logging
from Balances import Balances  # import class that defines balances
from Transaction import Transaction  # import class that defines transactions
import xml.etree.ElementTree as El  # imports library for parsing xml files
import datetime  # imports library for converting xml dates to dd/mm/yyyy

logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)  # configures the log


def load_file():
    logging.info("User was asked to input a file name.")
    carry_on = True
    amounts = []  # creates empty lists for storing values
    transaction_list = []
    while carry_on:
        file_input = input("Please enter the name of the file you'd like to search (with extension):\n")
        try:
            transaction_list = file_type(file_input)  # user inputs a file to be read
            amounts = Balances(transaction_list)
            carry_on = False  # exit loop when valid file name is entered
            enter_command()
        except FileNotFoundError:
            logging.info("The user entered an invalid file name. User entered: " + file_input)
            print("Sorry. That file name is invalid.")  # if the file isn't found in the local directory, the user is
            # asked for another file name
    return amounts, transaction_list


def file_type(filename):  # selects the type of file that has been loaded so that it can be parsed correctly
    if re.search(r".+\.(csv)", filename):
        logging.info("User entered a .csv file.")
        return read_csv(filename)
    elif re.search(r".+\.(json)", filename):
        logging.info("User entered a .json file")
        return read_json(filename)
    elif re.search(r".+\.(xml)", filename):
        logging.info("User entered a .xml file")
        return read_xml(filename)
    else:
        print("Sorry. I can't read that file. ")
        logging.info("User entered an unrecognised file type. The file entered was:" + filename)
        return load_file()


def read_open_file(filename, file):  # opens a file in read mode and logs this
    content = file.read()
    logging.info('Program initialised. User entered a valid file.')  # creates a log
    logging.info(filename + " has been opened in read mode.")
    return content


def read_csv(filename):  # function that opens and reads a csv file
    with open(filename, "r") as file:
        if file.mode == "r":  # checks that file is open in read mode
            content = read_open_file(filename, file)
            rows = re.findall(r"(\d{2}\/\d{2}\/\d{4}),([^,]+),([^,]+),([^,]+),([^,]+)\n\b", content)  # regex search
            # that groups data from each column

            transactions = []
            for csv_row in rows:
                transactions.append(Transaction.from_csv(csv_row))  # formats data into standard internal transaction
                # class format

            logging.info(filename + " has been read and closed.")
            return transactions


def read_json(filename):  # function that opens and reads a json file
    with open(filename, "r") as file:
        if file.mode == "r":  # checks that file is open in read mode
            content = read_open_file(filename, file)
            rows = re.findall(
                r"""".+": "(\d{4}-\d{2}-\d{2})",\n {4}".+": "(.+ ?.*)",\n {4}".+": "(.+ ?.*)",\n {4}".+": "(.+ ?.*)",\n {4}".+": (\d+.?\d*)""",
                content)  # regex search that groups data from each column

            transactions = []
            for json_transaction in rows:
                transactions.append(Transaction.from_json(json_transaction))  # formats data into standard internal
                # transaction class format

            logging.info(filename + " has been read and closed.")
            return transactions


def read_xml(filename):  # function that opens an xml file
    with open(filename, "r") as file:
        if file.mode == "r":  # checks that file is open in read mode
            content = El.parse(filename)  # parses the xml file using the element tree library
            root = content.getroot()  # finds the root of the file
            rows = []
            old_time = datetime.date(1900, 1, 1)  # for formatting xml's serial number dates

            for i in range(0, 149):  # there are 149 transactions
                new_time = old_time + datetime.timedelta(days=int(root[i].get("Date")))  # formats date to dd/mm/yyyy
                date = new_time.strftime("%d/%m/%y")
                from_person = root[i][2][0].text  # collects relevant data from file
                to_person = root[i][2][1].text
                narrative = root[i][0].text
                value = root[i][1].text

                rows.append((date, from_person, to_person, narrative, value))

            transactions = []
            for xml_transaction in rows:
                transactions.append(Transaction.from_xml(xml_transaction))  # formats data into standard internal
                # transaction class format

            logging.info(filename + " has been read and closed.")
            return transactions


def enter_command():  # presents command menu to the user
    logging.info("User was asked to select a command.")
    print("\nPlease type a command from the following list: \n"
          "1. List All \n2. List Account \n3. Help \n4. Quit")


def list_all(balances):  # function for listing all names and their net balances
    logging.info("List All function complete.")
    balances.display()

    return balances


def filter_transactions(account_name, transactions):  # filters transactions leaving ones only for the requested account
    logging.info("User selected List Account function for " + account_name)
    transaction_dict = {}  # creates an empty dictionary
    counter = 0  # initiates a counter
    for transaction in transactions:
        if transaction.owing == account_name:  # if someone has a transaction where they are owe money, add to dict
            transaction_dict[counter] = transaction
            counter += 1  # advance counter
            print(transaction.date, transaction.owed, transaction.owing,
                  "£" + format(float(transaction.amount), ".2f"))  # prints the transactions
        if transaction.owed == account_name:  # if someone has a transaction where they are owed money, add to dict
            transaction_dict[counter] = transaction
            counter += 1
            print(transaction.date, transaction.owed, transaction.owing,
                  "£" + format(float(transaction.amount), ".2f"))  # prints the transactions
    logging.info(account_name + "'s account contained " + str(counter) + " transactions")


def list_account(account_name, transactions, balances):  # function that prints a list of all transactions and net
    # balance for a person
    filter_transactions(account_name, transactions)

    logging.info("Total balance for " + account_name + " is being calculated.")
    balances.individual_display(account_name)  # prints full list of balances
    logging.info("List account function was completed for " + account_name)


def initiate_commands():
    amounts, transaction_list = load_file()  # loads file and pulls out relevant amounts
    cont = True  # allows user to exit at some point
    continu = True
    while cont:
        command = input()
        if command.lower() == "list all" or command.lower() == "listall" or command == "1":  # user
            # chooses a command
            logging.info("User selected the List All function.")
            list_all(amounts)
            enter_command()
        elif re.search(r"[Ll]ist ?[Aa]ccount", command) or command == "2":  # checks that the user has entered the
            # correct command
            while continu:
                try:
                    choose_account = input("Please enter the name of the account you'd like to see:")
                    name = re.findall(r"([A-Z][a-z]* ?[A-Z]?[a-z]*?)\b", choose_account)[0]  # finds name of
                    # the account the user wants
                    continu = False
                except IndexError:
                    print("Sorry. That name was not recognised. Please try again, ensuring the first and last name are "
                          "capitalised.\n")
            print("Here are the transactions for " + name + ":\n")
            list_account(name, transaction_list, amounts)
            enter_command()
        elif command.lower() == "help" or command == "3":  # help command brings up menu of commands
            logging.info("User requested help. Help menu displayed.")
            enter_command()
        elif command.lower() == "quit" or command == "4":  # exits the loop
            print("Thanks for visiting!")
            logging.info("User quit the program.")
            cont = False
            logging.info("Program terminated.")
        else:
            print("Invalid Command\n")  # if a user enters an invalid command, the loop restarts
            logging.info(
                "User entered an invalid command and was asked to try again.  The command entered was: " + command)
            enter_command()


initiate_commands()
