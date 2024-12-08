#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdbool.h>

int main()
{
    int n;
    do
    {
        n = get_int("Enter a number : ");
    }
    while(n<=0||n>8);


    for (int i = 1; i <= n; i++)
    {
        for (int k = 0; k < n - i; k++)
        {
            printf(" ");
        }
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
