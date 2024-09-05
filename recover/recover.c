#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
 #include <stdbool.h>

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }
    char *File=argv[1];
    // Open the memory card
    FILE *card = fopen(File, "r");
    if (card==NULL)
    {
        printf(" can not open %s\n",File);
        return 2;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];
    bool found_jpg=false;
    int jpg_count=0;
    char jpg_name[8];

    FILE *outptr=NULL;

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, 512, card) == 512)
    {
        if(buffer[0]==0xFF && buffer[1]==0xD8 && buffer[2]==0xFF && (buffer[3] & 0xF0)==0xE0)
        {
            if (found_jpg)
            {
                fclose(outptr);
            }
            else
            {
                found_jpg=true;
            }

        sprintf(jpg_name,"%03d.jpg",jpg_count);
        outptr=fopen(jpg_name,"w");
        if (outptr==NULL)
        {
            fclose(card);
            printf("can not create %s \n",jpg_name);
            return 3;
        }
        jpg_count++;
        }
        if (found_jpg)
        {
            fwrite(buffer,512,1,outptr);
        }

    }

    fclose(card);
    if (found_jpg)
    {
       fclose(outptr);
    }
    return 0;
}
