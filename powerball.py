from collections import Counter
from statistics import mode
import random

class Employee:

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.whiteball_numbers = []
        self.powerball = None

    def append_whiteballs(self, num):
        '''
        Adds a whiteball number to an employee's choice of whiteballs and sorts their whiteball array.
        :param num: Employee picked whiteball number
        '''
        self.whiteball_numbers.append(num)
        self.whiteball_numbers.sort()

    def get_whiteballs(self):
        '''
        :return: Returns the whiteballs that an employee picked out
        '''
        whiteball_string = ''
        for i in range(len(self.whiteball_numbers)):
            if (i==len(self.whiteball_numbers)-1):
                if (len(self.whiteball_numbers) > 1):
                    whiteball_string += ("and " + str(self.whiteball_numbers[i]))
                else:
                    whiteball_string += str(self.whiteball_numbers[i])
            else:
                whiteball_string += (self.whiteball_numbers[i] + ', ')

        return whiteball_string


def input_whiteball_message(whiteball_index, employee):
    '''
    :param whiteball_index: nth number being inserted into whiteball array
    :param employee: employee object
    :return: employee object with new whiteball numbers added
    '''
    whiteball_range = range(1,70)
    user_number = ''
    while (not user_number.isdigit() or int(user_number) not in whiteball_range or user_number in
        employee.whiteball_numbers):
        if whiteball_index == '1st':
            user_number = input("Select " + whiteball_index + " # (1 thru 69): ")
        else:
            user_number = input("Select " + whiteball_index + " # (1 thru 69 excluding " + employee.get_whiteballs()
                                + "): ")
    employee.append_whiteballs(user_number)
    return employee


def input_powerball_message(employee):
    '''
    Produces a user input message to create a powerball number.
    :param employee: employee object
    :return: employee object with powerball number added
    '''
    powerball_range = range(1,27)
    powerball = input('select Power Ball # (1 thru 26): ')
    while (not powerball.isdigit() or int(powerball) not in powerball_range):
        powerball = input('select Power Ball # (1 thru 26): ')
    employee.powerball = powerball
    return employee

def enter_powerball_info():
    '''
    Asks an employee to enter in their first/last name then asks them for their whiteball/powerball choices.
    Creates an employee object with this information.
    :return: Return an employee object containing their names and ball choices.
    '''
    first_name = input('Enter First Name: ')
    last_name = input('Enter Last Name: ')
    employee = Employee(first_name, last_name)
    employee = input_whiteball_message("1st", employee)
    employee = input_whiteball_message("2nd", employee)
    employee = input_whiteball_message("3rd", employee)
    employee = input_whiteball_message("4th", employee)
    employee = input_whiteball_message("5th", employee)
    employee = input_powerball_message(employee)

    return employee


def winning_powerballs(employees):
    '''
    Takes list of employee objects and uses their powerball number choices to determine the winning numbers.
    :param employees: List of employees who are in the powerball lottery
    :return: returns the winning whiteball numbers and powerball number
    '''
    whiteball_list = []
    # Group up all the employee whiteball numbers into a single array of all whiteball numbers
    for employee in employees:
        whiteball_list.extend(employee.whiteball_numbers)
    # Create a dict that numbers the occurrences of each whiteball value.
    whiteball_number_counts = (Counter(whiteball_list))
    # Make a copy of the whiteball_number_counts so it can be iterated through while making adjustments.
    whiteball_number_count_copy = dict(whiteball_number_counts)
    # Set a count of 5 which decrements by 1 each time a winning whiteball number is decided.
    count = 5
    winning_whiteballs = []
    for key, value in whiteball_number_count_copy.items():
        if count > 0:
            if value > 1:
                winning_whiteballs.append(key)
                del whiteball_number_counts[key]
                count -= 1
    if count > 0:
        allowed_randoms = list(range(1, 69))
        for i in winning_whiteballs:
            allowed_randoms.remove(int(i))

        # After counting duplicates in each list fill up the rest of the winning powerball numbers with random integers
        while (count > 0):
            random_number = random.choice(allowed_randoms)
            winning_whiteballs.append(random_number)
            allowed_randoms.remove(random_number)
            count -= 1

    # Loop through all employee powerball choices and find the most common one. Generate random powerball number
    # if there's no most common.
    powerball_choices = []
    for employee in employees:
        powerball_choices.append(employee.powerball)
        try:
            winning_powerball = mode(powerball_choices)
        except:
            winning_powerball = random.randrange(1, 26)

    return winning_whiteballs,winning_powerball


def display_employees(employees):
    '''
    Display the names and powerball numbers of employees participating in event.
    :param employees: List of employees
    '''
    for employee in employees:
        print(employee.first_name + " " + employee.last_name + " ", end='')
        print(*employee.whiteball_numbers, sep=' ', end='', flush=True)
        print(" Powerball: " + str(employee.powerball))


def display_winning_powerball(winning_whiteballs, winning_powerball):
    '''
    displays and formats the winning whiteball numbers and winning powerball numbers
    '''
    print('Powerball winning number: ')
    print(*winning_whiteballs, sep=' ', end='', flush=True)
    print(" Powerball: " + str(winning_powerball))


def main():
    employee_list = []
    employee_input = input('Would you like to enter in a new employee? y/n ')
    while (employee_input == 'y'):
        employee = enter_powerball_info()
        employee_list.append(employee)
        employee_input = input('Would you like to enter in a new employee? y/n ')
        if (employee_input == 'n'):
            display_employees(employee_list)
            winning_whiteballs, winning_powerball = winning_powerballs(employee_list)
            display_winning_powerball(winning_whiteballs, winning_powerball)

if __name__ == '__main__':
    main()

