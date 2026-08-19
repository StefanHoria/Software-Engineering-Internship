try:
    age = int(input("Enter your age: "))
    income = 20000
    risk = income / age
    print(age)
except ZeroDivisionError:
    print("You can't divide by zero")
except ValueError:
    print("You didn't enter a number.")