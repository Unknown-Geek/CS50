// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    uint8_t header[HEADER_SIZE];
    if(fread(header, sizeof(uint8_t), HEADER_SIZE, input) != HEADER_SIZE)
    {
        printf("Could not read header.");
        fclose(input);
        fclose(output);
        return 1;
    }

    if(fwrite(header, sizeof(uint8_t), HEADER_SIZE, output)!= HEADER_SIZE)
    {
        printf("Could not write header.");
        fclose(input);
        fclose(output);
        return 1;
    }


    // Create a buffer for a single sample
    int16_t buffer;

    // Read single sample from input into buffer
    while(fread(&buffer, sizeof(int16_t), 1, input))
    {
        // Update volume of sample
        buffer = (int16_t) (buffer * factor);

        // Write updated sample to new file
        if(fwrite(&buffer, sizeof(int16_t), 1, output) != 1)
        {
            fclose(input);
            fclose(output);
            return 1;
        }
    }
    fclose(input);
    fclose(output);
}
