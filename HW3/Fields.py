#HW3
#Dhruv Aggarwal
#aggarw45  
#2/6/20
import os

number = input("Please enter a number to check if it's a ring or a field: ")
check_number = int(number)

if check_number == 1:
    print("ring")
else:
    for each in range(2,check_number):
        if (check_number % each) == 0:
            print("ring")
            break
    else:
            print("field")        