import os
from tempfile import NamedTemporaryFile
import shutil
import csv as csv_m


def welcome(name=''):
    print(f"Welcome,{name}." if len(name) > 0 else "Welcome to our bank")


class CSV:
    def __init__(self):
        self.data = ['null', 'null', 'null']
        self.filename = 'users.csv'

    def get_csv_data(self, usr_number):
        try:
            self.data = open(self.filename, 'r').read().split('\n')[usr_number - 1].split(',')
            return True
        except IndexError:
            return False

    def user_login(self, acc_number):
        if self.get_csv_data(acc_number) is True:
            return self.data[1]
        else:
            return ""

    def get_balance(self):
        return self.data[2]

    def set_balance(self, new_balance):
        self.data[2] = new_balance
        return True

    # Bonus Task
    def update_user_data(self, acc_num):
        temp_file = NamedTemporaryFile(mode='w', delete=False)

        fields = ['ID', 'Name', 'Balance']

        with open(self.filename, 'r') as csv_file, temp_file:
            reader = csv_m.DictReader(csv_file, fieldnames=fields)
            writer = csv_m.DictWriter(temp_file, fieldnames=fields)
            for row in reader:
                if row['ID'] == str(acc_num):
                    row['Name'], row['Name'], row['Balance'] = self.data[0], self.data[1], self.data[2]
                row = {'ID': row['ID'], 'Name': row['Name'], 'Balance': row['Balance']}
                writer.writerow(row)

        shutil.move(temp_file.name, self.filename)


class BankSystem:
    def __init__(self):
        self.csv = None
        self.menuOption = ['Show current balance', 'Make a deposit', 'Make withdrawal', 'Exit the system']

    def init__csv(self, obj):
        self.csv = obj

    def show_menu(self):
        no_of_options = len(self.menuOption)
        for i in range(no_of_options):
            print(f"{i + 1}. {self.menuOption[i]}")

    def get_user_choice(self):
        choice = -1
        no_of_options = len(self.menuOption)
        while choice < 1 or choice > no_of_options:
            try:
                choice = int(input("Please choose your operation :"))
            except ValueError:
                return 0
            if choice < 1 or choice > no_of_options:
                print("Try again, Please enter valid number")
        return choice

    def get_menu_option(self, num):
        # if user didn't input anything
        if num < 1:
            return ""
        return self.menuOption[num - 1]

    def show_current_balance(self):
        return self.csv.get_balance()

    def make_a_deposit(self, dep_amount):
        if dep_amount < 1:
            return False
        else:
            self.csv.set_balance(str(float(csv.get_balance()) + float(dep_amount)))
            return True

    def make_withdrawal(self, wd_amount):
        if wd_amount < 1 or wd_amount > float(csv.data[-1]):
            return False
        else:
            self.csv.set_balance(str(float(csv.get_balance()) - float(wd_amount)))
            return True


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear Terminal cross-platform
    csv = CSV()
    # Welcome Screen
    welcome()

    # ask user for account number until a valid number entered
    usr_name = ""
    acc_no = None
    while not usr_name:
        try:
            acc_no = int(input("Please enter your account number :"))
            usr_name = csv.user_login(acc_no)
        except ValueError:
            print("Please try again and enter a valid account number")
        else:
            if not usr_name:
                print("Please try again and enter a valid account number")

    # Logged in successfully
    if usr_name != "":
        # initiate the system
        user = BankSystem()
        # Sync user data
        user.init__csv(csv)

        order = ''
        while order != 'Exit the system':

            # Show menu and getting a user choice
            # Welcome the user
            welcome(usr_name)
            user.show_menu()
            order = user.get_menu_option(user.get_user_choice())

            # show balance
            if order == 'Show current balance':
                print(user.show_current_balance())

            # make a deposit
            elif order == 'Make a deposit':
                suc = False
                try:
                    amount = float(input("Please enter the amount to deposit: "))
                    suc = user.make_a_deposit(amount)
                except ValueError:
                    print("deposit failed !")
                    print("Please enter valid amount to deposit.")
                else:
                    if suc is True:
                        print("Deposit was successful")
                    print(f"New balance : {user.show_current_balance()}")

            # Make a withdrawal
            elif order == 'Make withdrawal':
                try:
                    amount = float(input("Please enter the amount to withdraw: "))
                    suc = user.make_withdrawal(amount)
                except ValueError:
                    print("Withdrawal failed !")
                    print("Please enter valid amount to deposit.")
                else:
                    if suc is True:
                        print("Withdrawal was successful!")
                        print(f"New balance : {user.show_current_balance()}")
                    else:
                        print("Withdrawal was failed")
                        print(f"Your current balance is {user.show_current_balance()}")

            elif order == 'Exit the system':
                csv.update_user_data(acc_no)
                print("")
                print(f"Good bye, {usr_name}...")
                break
            else:
                print("Please try again and enter a valid operation number")

            # Clear the screen
            print("")
            input("Press any key to clear the screen and continue ...")
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear Terminal cross-platform
