# Step 1: Create a set with your favorite numbers
my_fav_numbers = set()

# Step 2: Add two new numbers
my_fav_numbers.add(73)
my_fav_numbers.add(98)
my_fav_numbers.add(99)
my_fav_numbers.add(2)

# Step 3: Remove one number (simulate "last number")
my_fav_numbers.pop()


# Step 4: Create a set with your friend’s favorite numbers
friend_fav_numbers = set()
friend_fav_numbers.add(45)  # Adding an additional favorite number
friend_fav_numbers.add(33)  # Adding an additional favorite number
friend_fav_numbers.add(5)  # Adding an additional favorite number

# Step 5: Combine both sets
our_fav_numbers = my_fav_numbers.union(friend_fav_numbers)

# Output the result
print(our_fav_numbers)
