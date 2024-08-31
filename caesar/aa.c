#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    char a=get_char("Enter:");
    int b=(int) a;
    printf("%i  ",b);
}
        string plaintext = get_string("plaintext: ");
        printf("ciphertext: ");

        // Reads the plaintext and converts it it ciphertext
        for (int i = 0; i < strlen(plaintext); i++)
        {
            // Converts all the lower letter alphabets
            if (plaintext[i] >= 'a' && plaintext[i] <= 'z')
            {
                printf("%c", ((((plaintext[i] - 'a') + k) % 26) + 'a'));
            }
            // Converts all the upper letter alphabets
            else if (plaintext[i] >= 'A' && plaintext[i] <= 'Z')
            {
                printf("%c", ((((plaintext[i] - 'A') + k) % 26) + 'A'));
            }
            // Returns any character other thatn alphabets as such
            else
            {
                printf("%c", plaintext[i]);
            }
        }
        printf("\n");
        return 0;
