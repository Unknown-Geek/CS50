#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    int c1 = 0, c2 = 0;
    int temp, n1 ,n2,i;
    int list[26] = {1,3,3,2,1,4,2,4,1,8,5,1,3,1,1,3,10,1,1,1,1,4,4,8,4,10};

    string s1 = get_string("Enter string 1: ");
    string s2 = get_string("Enter string 2: ");

    for(i = 0, n1 = strlen(s1); i<n1; i++)
    {
        if(isalpha(s1[i]))
        {
            temp = toupper(s1[i]) - 'A';
            c1 += list[temp];
        }
    }

    for(i = 0, n2 = strlen(s2); i <n2; i++)
    {
        if(isalpha(s2[i]))
        {
            temp = toupper(s2[i]) - 'A';
            c2 += list[temp];
        }
    }

    if(c1 > c2)
        printf("Player 1 wins!\n");
    else if(c1 == c2)
        printf("Tie!\n");
    else
        printf("Player 2 wins!\n");

    return 0;
}
