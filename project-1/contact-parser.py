""" A simple program parsing a comma delimted csv file.

This program parses a csv file at a filepath given by the user. It both stores
the data in a Person class, and saves it as a pickle file. Then this pickle
file is displayed.

Example database:
	Last,First,Middle Initial,ID,Office phone
	Smith,Smitty,S,WH1234,5557771212
	WILLIAMS,WITTY,W,S4454,555-877.4321
	Luka,Luka,L,OF4321,555.888.3456
	jason,jake,,WH409,555 777 2094
	Krishna,krishna,k,SA9384,555 888 0093

Example usage:
	python contact-parser.py data/data.csv

"""


import sys      # to get the system parameter
import pathlib  # to parse and access filepath
import pickle   # to store the data in a binary
import re		# include regex for data checking


class Person:
    """ Stores information about a person, their name, phone number, and id.

    """

    def __init__(self, last, first, mi, id_num, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id_num = id_num  # Not id as to avoid using built in function name
        self.phone = phone

    def display(self):
        print("Employee id: " + self.id_num + "\n" +
              "\t" + self.first + " " + self.mi + " " + self.last + "\n" +
              "\t" + self.phone)


def parse(line):
    """ Parses and cleans a line of data to initialize a Person object.

    """
    # Assumes content is a string

    tokens = line.split(',')

    # Captilize the names if the aren't already. Fun fact, I used regex to check
    # this originally, but it seems checking for fun unicode characters wasn't
    # working on here too well so I went back to basics
    tokens[0] = tokens[0].capitalize()
    tokens[1] = tokens[1].capitalize()

    # Set initial to 'X' if it doesn't exist, or set to be one upper case
    # character if not
    if not tokens[2]:
        tokens[2] = "X"
    else:
        tokens[2] = tokens[2][0].upper()

    tokens[3] = fix_id(tokens[3])

    tokens[4] = fix_phone(tokens[4])

    # Unpack tokens list and initialize as person
    return Person(*tokens)


def fix_id(id_num):
    """ Checks ID is 2 capital letter & 4 numbers, otherwise takes ID input.

    """
    # Compile the pattern since we may have to use it multiple times
    pattern = re.compile(r'^[A-Z]{2}\d{4}$')
    while not pattern.match(id_num):

        print("ID invalid: " + id_num)
        id_num = input()
    return id_num


def fix_phone(phone):
    """ Formats a phone number to have 3 digits - 3 digits - 4 digits.

    """
    # If the phone number is not in the form ###-###-####, create a phone number
    # assuming that there were 3 separate sections of numbers of length 3, 3, 4.
    if not re.match(r'^\d{3}-\d{3}-\d{4}', phone):
        phone = re.sub(r"(\d{3}).*(\d{3}).*(\d{4})", r"\1-\2-\3", phone)
    return phone


def read_file_name(filepath):
    """ Reads data from a filepath into a list of lines from the file.

    """
    with open(pathlib.Path.cwd().joinpath(filepath), 'r') as f:
        next(f)
        line_list = [line.rstrip() for line in f]
    return line_list


def main():
    """ Creates Person objects from given file, stores them, and displays them.

    """
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        exit()

    fp = sys.argv[1]
    data = read_file_name(fp)

    person_dict = {}

    for line in data:
        person = parse(line)
        person_dict[person.id_num] = person

    # Save into pickle file as an example of storing python data
    pickle.dump(person_dict, open('dict.p', 'wb'))

    # Then immediately open to read the contents of the saved dictionary
    person_dict_2_electric_boogaloo = pickle.load(open('dict.p', 'rb'))

    # Display the data
    print("Employee List:\n")
    for person in person_dict_2_electric_boogaloo.values():
        person.display()
        print()  # Add a newline

    # Complete!
    exit()


# Run as script
if __name__ == '__main__':
    main()
