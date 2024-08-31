#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int calculate_letters(string text);
int calculate_words(string text);
int calculate_sentences(string text);

int main(void)
{
    // Taking input from the user
    string text = get_string("Text: ");
    float letters = (float) calculate_letters(text);
    float words = (float) calculate_words(text);
    float sentences = (float) calculate_sentences(text);
    // caclulating the Coleman-Liau index
    float L = (letters / words) * 100.00;
    float S = (sentences / words) * 100.00;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}
// creating a function to calculate letters
int calculate_letters(string text)
{
    int letters = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters += 1;
        }
    }
    return letters;
}
// creating a function to calculate words
int calculate_words(string text)
{
    int words = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isspace(text[i]))
        {
            words += 1;
        }
    }
    return words;
}
// creating a function to calculate sentences
int calculate_sentences(string text)
{
    int sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '!' || text[i] == '.' || text[i] == '?')
        {
            sentences += 1;
        }
    }
    return sentences;
}
