# first
for number in range(1, 21):  # range(1, 21) goes from 1 to 20
    print(number)

# second
for index, number in enumerate(range(1, 21)):  # index starts at 0
    if index % 2 == 0:  # check if index is even
        print(number)
