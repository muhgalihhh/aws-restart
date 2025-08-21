myString = "This is a string."
print(myString)

print(type(myString))

print(myString + " is of the data type " + str(type(myString)))

# Working string with concatenation

firstString = "water"
secondString = "fall"
thirdString = firstString + secondString
print(thirdString)

# Working with input strings

name = input('What is your name?')

print(name)

# Formatting input strings

color = input("What is your favorite color?  ")
animal = input("What is your favorite animal?  ")

print("{}, you like a {} {}!".format(name,color,animal))