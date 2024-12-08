import cs50
n = 0
while(1):
    try:
        change = cs50.get_float("Enter the change : ")
        if change>0:
            break;
        else:
            print("Enter a valid number")
    except ValueError:
                print("Invalid input. Please enter a number.")

change = int(change*100)


n += change // 25;
change %= 25;

n += change // 10;
change %= 10;

n += change // 5;
change %= 5;

n += change;

print(n)
