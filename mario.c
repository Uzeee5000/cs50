#include <stdio.h>
#include<cs50.h>
void print_row(int bricks, int rows);
int main(void)
{
    int n;
    do
    {
        n= get_int("Size: ");
    }

    while(n<1||n>8);

    for(int i=0;i<n;i++)
    {
        print_row(i+1,n);
    }

}
void print_row(int bricks, int rows)
{
    for (int i = 0; i < rows - bricks; i++)
    {
        printf(" ");
    }
    for (int i = 0; i < bricks; i++)
    {
        printf("#");
    }
    printf("\n");
}
