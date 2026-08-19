"""""
has_high_income = False
has_good_credit = True
has_criminal_record = True

if has_good_credit and not has_criminal_record:
    print("Eligible for Loan!")


if has_high_income or has_good_credit:
    print("Eligible for Loan!")
"""
    #Comparison Operators
"""""
temperature = 30

if temperature != 30:
    print("It`s a hot day")
else:
    print("It`s not a hot day")

"""
name  = "Jay"
print(len(name))

if len(name) < 3:
    print("Name must be at least 3 characters long")
elif len(name) > 50:
    print("Name cannot exceed 50 characters")
else:
    print("Name looks good!")
