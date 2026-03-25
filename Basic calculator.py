# Basic Calculator Program
# Performs addition, subtraction, multiplication, and division

import select
def display_menu():
    """Display the calculator menu"""
    print("\n" + "="*40)
    print("         BASIC CALCULATOR")
    print("="*40)
    print("Select operation:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (×)")
    print("4. Division (÷)")
    print("5. Exit")
    print("="*40)

def get_numbers():
    """Get two numbers from user"""
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        return num1, num2
    except ValueError:
        print("❌ Invalid input! Please enter numbers only.")
        return None, None

def add(a, b):
    """Addition"""
    return a + b

def subtract(a, b):
    """Subtraction"""
    return a - b

def multiply(a, b):
    """Multiplication"""
    return a * b

def divide(a, b):
    """Division with error handling"""
    if b == 0:
        return "❌ Error! Division by zero is not allowed."
    return a / b

def calculate():
    """Main calculator function"""
    while True:
        display_menu()
        
        # Get user choice
        choice = input("Enter your choice (1-5): ")
        
        # Exit condition
        if choice == '5':
            print("\n👋 Thank you for using the calculator. Goodbye!")
            break
        
        # Validate choice
        if choice not in ['1', '2', '3', '4']:
            print("❌ Invalid choice! Please select 1-5.")
            continue
        
        # Get numbers
        num1, num2 = get_numbers()
        if num1 is None or num2 is None:
            continue
        
        # Perform calculation based on choice
        print("\n" + "-"*40)
        print("RESULT:")
        
        if choice == '1':
            result = add(num1, num2)
            print(f"{num1} + {num2} = {result}")
        
        elif choice == '2':
            result = subtract(num1, num2)
            print(f"{num1} - {num2} = {result}")
        
        elif choice == '3':
            result = multiply(num1, num2)
            print(f"{num1} × {num2} = {result}")
        
        elif choice == '4':
            result = divide(num1, num2)
            if isinstance(result, str):  # Error message
                print(result)
            else:
                print(f"{num1} ÷ {num2} = {result}")
        
        print("-"*40)
        
        # Ask if user wants to continue
        again = input("\nDo you want to perform another calculation? (y/n): ")
        if again.lower() != 'y':
            print("\n👋 Thank you for using the calculator. Goodbye!")
            break

# Run the calculator
if __name__ == "__main__":
    calculate()