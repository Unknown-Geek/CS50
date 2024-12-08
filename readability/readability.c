#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <ctype.h>

int main(){
    string str = get_string("Text: ");
    int n = strlen(str);
    float L, S, index;
    int letters = 0, words = 1, sen = 0; // Initialize words to 1

    for(int i = 0; i < n; i++)
    {
        if (isalpha(str[i]) != 0)
            letters++;
        else if (str[i] == ' ')
            words++;
        else if(str[i] == '.' || str[i] == '!' || str[i] == '?')
            sen++;
    }

    L = (float) letters / words * 100;
    S = (float) sen / words * 100;
    index = (0.0588 * L) - (0.296 * S) - 15.8;
    int grade = round(index);

    if (grade < 1)
        printf("Before Grade 1\n");
    else if (grade >= 16)
        printf("Grade 16+\n");
    else
        printf("Grade %d\n", grade);
}
