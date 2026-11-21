# ==============================================================
# Project: ATM Management System
# Subject: Programming Fundamentals and Logic Building Using Python
# Language: Python 3
# ==============================================================

import os

# Path to the data file in the current directory (resolved absolutely)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
file_path = os.path.join(BASE_DIR, "atm.txt")

# Global variables
pin = "1234"
balance = 10000
transactions = []


def load_data():
    """Loads account data and transaction history from atm.txt."""
    global pin, balance, transactions
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
                if len(lines) >= 2:
                    pin = lines[0]
                    balance = int(lines[1])
                    transactions = lines[2:]
                else:
                    # If file is empty or corrupted, reset with default values
                    pin = "1234"
                    balance = 10000
                    transactions = []
                    save_data()
        else:
            # Create default file if it doesn't exist
            pin = "1234"
            balance = 10000
            transactions = []
            save_data()
    except Exception as e:
        print("Error reading file:", e)
        pin = "1234"
        balance = 10000
        transactions = []
        save_data()


def save_data():
    """Saves balance and transactions to file after every operation."""
    try:
        with open(file_path, "w") as f:
            f.write(str(pin) + "\n")
            f.write(str(balance) + "\n")
            for t in transactions:
                f.write(t + "\n")
    except Exception as e:
        print("Error saving to file:", e)


def verify_pin():
    """Verifies PIN with a maximum of 3 attempts using a loop."""
    attempts = 3
    while attempts > 0:
        entered_pin = input("Enter your PIN: ").strip()
        if entered_pin == pin:
            print("Login successful")
            return True
        else:
            attempts -= 1
            if attempts > 0:
                print(f"Invalid PIN. Attempts left: {attempts}")
            else:
                print("Account locked. Exiting...")
                return False


def check_balance():
    """Displays the current balance."""
    print(f"Current Balance: {balance}")


def deposit():
    """Handles deposit operation."""
    global balance
    try:
        amount_input = input("Enter amount to deposit: ").strip()
        amount = int(amount_input)

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        balance = balance + amount
        transactions.append(f"Deposit {amount} | Balance: {balance}")
        save_data()
        print(f"Deposit successful. New Balance: {balance}")

    except ValueError:
        print("Invalid amount. Please enter numbers only.")


def withdraw():
    """Handles withdrawal operation."""
    global balance
    try:
        amount_input = input("Enter amount to withdraw: ").strip()
        amount = int(amount_input)

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        if amount > balance:
            print("Insufficient balance!")
            return

        balance = balance - amount
        transactions.append(f"Withdraw {amount} | Balance: {balance}")
        save_data()
        print(f"Withdrawal successful. New Balance: {balance}")

    except ValueError:
        print("Invalid amount. Please enter numbers only.")


def mini_statement():
    """Displays mini statement with transaction history."""
    if len(transactions) == 0:
        print("No transactions yet.")
    else:
        for i in range(len(transactions)):
            print(f"{i + 1}. {transactions[i]}")


def main():
    load_data()

    # User login
    if not verify_pin():
        return

    # Menu loop
    while True:
        print("\n--- ATM Menu ---")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Mini Statement")
        print("5. Exit")

        try:
            choice_input = input("Enter your choice (1-5): ").strip()
            choice = int(choice_input)

            if choice == 1:
                check_balance()
            elif choice == 2:
                deposit()
            elif choice == 3:
                withdraw()
            elif choice == 4:
                mini_statement()
            elif choice == 5:
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Please choose between 1 and 5.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSession ended. Goodbye!")
