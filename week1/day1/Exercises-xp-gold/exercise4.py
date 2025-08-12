names = ["Samus", "Cortana", "V", "Link", "Mario", "Cortana", "Samus"]

input_name = input("Enter a name to search for: ").capitalize()

if input_name in names:
    indexes = [i for i, name in enumerate(names) if name == input_name]
    print(f"{input_name} found at indexes: {indexes}")
else:
    print(f"{input_name} not found.")
