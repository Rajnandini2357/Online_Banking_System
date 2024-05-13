
#downloads

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, QStackedWidget, QInputDialog

class Account:
    def __init__(self, account_number, balance=10000):
        self.account_number = account_number
        self.balance = balance
   
    def deposit(self, amount):
        self.balance += amount
   
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            return False

class Customer:
    def __init__(self, username, password, account):
        self.username = username
        self.password = password
        self.account = account
   
    def transfer(self, recipient, amount):
        if self.account.withdraw(amount):
            recipient.account.deposit(amount)
            return True
        else:
            return False

class Transaction:
    @staticmethod
    def create_account(account_number):
        return Account(account_number)

class CreateAccountPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.create_account_button = QPushButton('Create Account')
        self.create_account_button.clicked.connect(self.create_account)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.create_account_button)

        self.setLayout(layout)

    def create_account(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            account = Transaction.create_account(f"{username}_account")
            customer = Customer(username, password, account)
            customers.append(customer)
            self.parent().setCurrentIndex(1)  # Switch to the login page
        else:
            self.show_message("Error", "Username and password cannot be empty.")

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        for customer in customers:
            if customer.username == username and customer.password == password:
                main_page.update_customer(customer)
                self.parent().setCurrentIndex(2)  # Switch to the main page
                return
        self.show_message("Login Failed", "Invalid username or password.")

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.customer = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.transfer_button = QPushButton('Transfer Funds')
        self.transfer_button.clicked.connect(self.transfer_funds)

        self.withdraw_button = QPushButton('Withdraw')
        self.withdraw_button.clicked.connect(self.withdraw_funds)

        self.deposit_button = QPushButton('Deposit')
        self.deposit_button.clicked.connect(self.deposit_funds)

        self.check_balance_button = QPushButton('Check Balance')
        self.check_balance_button.clicked.connect(self.check_balance)

        self.balance_label = QLabel()

        layout.addWidget(self.transfer_button)
        layout.addWidget(self.withdraw_button)
        layout.addWidget(self.deposit_button)
        layout.addWidget(self.check_balance_button)
        layout.addWidget(self.balance_label)

        self.setLayout(layout)

    def update_customer(self, customer):
        self.customer = customer

    def transfer_funds(self):
        recipient_username, ok = QInputDialog.getText(self, 'Transfer Funds', 'Enter recipient username:')
        if ok:
            amount, ok = QInputDialog.getInt(self, 'Transfer Funds', 'Enter amount:')
            if ok:
                recipient = next((c for c in customers if c.username == recipient_username), None)
                if recipient:
                    if self.customer.transfer(recipient, amount):
                        self.show_message("Transfer Successful", f"Transferred ${amount} to {recipient_username}.")
                    else:
                        self.show_message("Transfer Failed", "Insufficient balance.")
                else:
                    self.show_message("Error", f"Recipient '{recipient_username}' not found.")
   
    def withdraw_funds(self):
        amount, ok = QInputDialog.getInt(self, 'Withdraw Funds', 'Enter amount:')
        if ok:
            if self.customer.account.withdraw(amount):
                self.show_message("Withdrawal Successful", f"Withdrew ${amount}.")
            else:
                self.show_message("Withdrawal Failed", "Insufficient balance.")

    def deposit_funds(self):
        amount, ok = QInputDialog.getInt(self, 'Deposit Funds', 'Enter amount:')
        if ok:
            self.customer.account.deposit(amount)
            self.show_message("Deposit Successful", f"Deposited ${amount}.")

    def check_balance(self):
        self.balance_label.setText(f"Your balance is: ${self.customer.account.balance}")

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    customers = []

    stacked_widget = QStackedWidget()
    create_account_page = CreateAccountPage()
    login_page = LoginPage()
    main_page = MainPage()

    stacked_widget.addWidget(create_account_page)
    stacked_widget.addWidget(login_page)
    stacked_widget.addWidget(main_page)

    stacked_widget.setWindowTitle('Online Banking System')
    stacked_widget.setGeometry(100, 100, 400, 200)
    stacked_widget.show()

    sys.exit(app.exec_())
