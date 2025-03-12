evencounter = 0
while 1:
    num = int(input("please input an integer into the database : "))

    if num % 2 == 0:
        evencounter += 1

    print(" there are", evencounter , "even numbers in the database so far")

    if evencounter == 3:
        break

print(" We get", evencounter , "even numbers in our database .")
print("please stop inputting new data in the data base")