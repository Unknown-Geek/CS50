#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <ctype.h>

char rotate(char c, int n)
{
    if (!isalpha(c))
        return c;

    char base = islower(c) ? 'a' : 'A';
    return (c - base + n) % 26 + base;
}

int main(int argc, char* argv[]){
    int key;
    if(argc != 2)
    {
        printf("Only one argument supported.\n");
        return 1;
    }
    for (int i = 0; argv[1][i] != '\0'; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    key = atoi(argv[1]);
    string s = get_string("plaintext: ");
    int n = strlen(s);
    int val;
    char cipher_text[n+1];

    printf("ciphertext: ");
    for(int i = 0; i<n; i++)
    {
        cipher_text[i] = rotate(s[i],key);
        printf("%c",cipher_text[i]);
    }
    cipher_text[n] = '\0';
    printf("\n");

}
