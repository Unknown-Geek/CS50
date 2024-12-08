import cs50
import math
str = cs50.get_string("Text: ")
n =  len(str)
letters = 0
words = 1
sen = 0

for i in range(n):
    if (str[i].isalpha() != 0):
        letters += 1
    elif (str[i] == ' '):
        words += 1
    elif(str[i] == '.' or str[i] == '!' or str[i] == '?'):
        sen += 1

L = float(letters / words * 100)
S = float(sen / words * 100)
index = (0.0588 * L) - (0.296 * S) - 15.8
grade = round(index)

if (grade < 1):
    print("Before Grade 1")
elif (grade >= 16):
    print("Grade 16+")
else:
    print("Grade", grade)

