import random

lower = "abcdefghijklmnopqrstuvwxyz"
upper = "abcdefghijklmnopqrstuvwxyz".upper()
numbers = "0123456789"
symbols = "[]{}()*;/,._-+="

all = lower + upper + numbers + symbols

length = int(input("Enter required length: "))
password = "".join(random.sample(all, length))
print(f"The generated password is '{password}'")