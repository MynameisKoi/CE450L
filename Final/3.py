print("Enter a number less than 10000: ", end="")
num = int(input())
# Display all prime number pair with difference of 2 between 1 and num
for i in range(1, num):
    # check prime number
    if i > 1:
        for j in range(2, i):
            if (i % j) == 0:
                break
        else:
            # check prime number pair with difference of 2
            if (i+2) > 1:
                for k in range(2, i+2):
                    if ((i+2) % k) == 0:
                        break
                else:
                    print(i, i+2)