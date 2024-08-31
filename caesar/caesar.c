#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int only_digits(string s);
void output(int k, string plaintext);

int main(int argc, string argv[])
{
    // Make sure program was run with just one command-line argument
    if(argc!=2 ||only_digits(argv[1])!=0)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Converting argv[1] from a `string` to an `int`
    int k=atoi(argv[1]);
    // Prompt user for plaintext
    string plaintext=get_string("plaintext:  ");

    //starts from here
    printf("ciphertext: ");
    output(k,plaintext);
    printf("\n");

}

// Make sure every character in argv[1] is a digit
int only_digits(string s)
{
    int a=0;
    for(int i=0, n=strlen(s);i<n;i++)
    {
        if (!isdigit(s[i]))
        {
        a+=1;
        }
    }
    return a;
}
//conversion in to cypher text
void output(int k, string plaintext)
{

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
        // Returns any character other than alphabets as it is
        else
        {
            printf("%c", plaintext[i]);
        }
    }
}


