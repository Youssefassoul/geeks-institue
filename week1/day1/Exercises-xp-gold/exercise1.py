# first method
month = int(input("Enter a month number (1-12): "))
if month >= 3 and month <= 5:
    print("It's Spring season!")
elif month >= 6 and month <= 8:
    print("It's Summer season!")
elif month >= 9 and month <= 11:
    print("It's Autumn season!")
elif month == 12 or month == 1 or month == 2:
    print("It's Winter season!")
else:
    print("Invalid month entered.")


# second method
month = int(input("Enter a month number (1 to 12): "))

if month in (3, 4, 5):
    season = "Spring"
elif month in (6, 7, 8):
    season = "Summer"
elif month in (9, 10, 11):
    season = "Autumn"
elif month in (12, 1, 2):
    season = "Winter"
else:
    season = "Invalid month entered."

if season:
    print(f"The season is {season}.")
else:
    print("Invalid month number.")
