"""""
customer = {
    "name": "John Smith",
    "age":30,
    "is_verified": True
}
customer["name"] = "jack smith"

print(customer["name"])
"""
phone = input("Enter a phone number: ")
digits_mapping = {
    "0":"Zero",
    "1":"One",
    "2":"Two",
    "3":"Three",
    "4":"Four",
    "5":"Five",
    "6":"Six",
    "7":"Seven",
    "8":"Eight",
    "9":"Nine",
}
output = ""
for ch in phone:
    output += digits_mapping.get(ch, "!") + " "
print(output)