while(1):
    try:
        n = int(input("Enter value of n : "))
        if 0<n<9:
            break;
        else:
            print("Enter a valid number")
    except ValueError:
                print("Invalid input. Please enter a number.")


for i in range(1,n+1):
    spaces = ' ' * (n - i)
    hashes = '#' * i
    print(f"{spaces}{hashes}")



