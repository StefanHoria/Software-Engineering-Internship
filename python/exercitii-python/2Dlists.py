matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
#matrix[0][1] = 20
#print(matrix[0][1])

"""""
for row in matrix:
    for item in row:
        print(item)
"""""
#numbers = [5, 2, 1, 7, 4, 5,10]
"""""
numbers.append(20)
print(numbers)

numbers.insert(0, 10)
print(numbers)

numbers.remove(5)
print(numbers)

#numbers.clear()
#print(numbers)

numbers.pop()
print(numbers)
"""
#print(numbers.index(50))
#print(50 in numbers)
#print(numbers.count(5))
#numbers.sort()
#numbers.sort(reverse=True)
#numbers.append(20)
#numbers2 = numbers.copy()
#print(numbers2)

numbers = [2, 2, 4, 6, 3, 4, 6, 1]
uniques = []

for number in numbers:
    if number not in uniques:
        uniques.append(number)
print(uniques)