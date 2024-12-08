#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

int count = 0;

typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

const unsigned int N = 26;

node *table[N];

bool check(const char *word)
{
    int hash_val = hash(word);
    node *cursor = table[hash_val];

    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
            return true;
        cursor = cursor->next;
    }
    return false;
}

unsigned int hash(const char *str)
{
    unsigned long sum = 0;
    for (int i = 0; str[i] != '\0'; i++)
    {
        sum += tolower(str[i]);
    }
    return sum % N;
}

bool load(const char *dictionary)
{
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
        return false;

    char word[LENGTH + 1];
    while (fscanf(source, "%s", word) != EOF)
    {
        node *new = malloc(sizeof(node));
        if (new == NULL)
        {
            fclose(source);
            return false;
        }

        strcpy(new->word, word);
        int hash_val = hash(word);
        new->next = table[hash_val];
        table[hash_val] = new;
        count++;
    }

    fclose(source);
    return true;
}

unsigned int size(void)
{
    return count;
}

bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
