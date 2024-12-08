#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define BLOCK_SIZE 512
#define FILENAME_SIZE 8

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 1;
    }

    int jpg_count = 0;
    char filename[FILENAME_SIZE];
    FILE *img = NULL;

    // Create a buffer for a block of data
    uint8_t buffer[BLOCK_SIZE];

    while (fread(buffer, BLOCK_SIZE, 1, card) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Close previous file if open
            if (img != NULL)
            {
                fclose(img);
            }

            // Create a new JPEG file
            snprintf(filename, FILENAME_SIZE, "%03i.jpg", jpg_count);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                fclose(card);
                fprintf(stderr, "Could not create JPEG file %s.\n", filename);
                return 1;
            }
            jpg_count++;
        }

        // Write to JPEG file if one is open
        if (img != NULL)
        {
            fwrite(buffer, BLOCK_SIZE, 1, img);
        }
    }

    // Close any remaining open files
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(card);

    return 0;
}
