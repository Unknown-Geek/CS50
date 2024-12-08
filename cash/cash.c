#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int n = 0;
    int change;
    do
    {
        change = get_int("Change owed: ");
    }
    while(change<0);

    // Calculate the number of quarters
    n += change / 25;
    change %= 25;

    // Calculate the number of dimes
    n += change / 10;
    change %= 10;

    // Calculate the number of nickels
    n += change / 5;
    change %= 5;

    // Calculate the number of pennies
    n += change;

    printf("%d\n", n);
}
