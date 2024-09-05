#include "helpers.h"
#include<math.h>
#include<string.h>

int min(int a, int b);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of red, green, and blue
            float average=round((image[i][j].rgbtBlue+image[i][j].rgbtGreen+image[i][j].rgbtRed)/3.0);
            // Update pixel values
            image[i][j].rgbtBlue=average;
            image[i][j].rgbtGreen=average;
            image[i][j].rgbtRed=average;
        }
    }
}
// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Compute sepia values
            float sepiaRed =round( .393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            float sepiaGreen =round( .349  * image[i][j].rgbtRed + .686  * image[i][j].rgbtGreen + .168  * image[i][j].rgbtBlue);
            float sepiaBlue =round( .272  * image[i][j].rgbtRed + .534  * image[i][j].rgbtGreen + .131  * image[i][j].rgbtBlue);

            // Update pixel with sepia values
            image[i][j].rgbtRed=min(sepiaRed,255);
            image[i][j].rgbtGreen=min(sepiaGreen,255);
            image[i][j].rgbtBlue=min(sepiaBlue,255);

        }
    }
}
// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    RGBTRIPLE temp;

    for (int i = 0; i < height; i++)
    {
        for (int x = 0; x < width / 2; x++)
        {
            temp = image[i][x];
            image[i][x] = image[i][width - x-1];
            image[i][width - x-1] = temp;
        }
    }
}
// Blur image

void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Temporary storage
    RGBTRIPLE temp[height][width];

    // Temp Image
    memcpy(temp, image, sizeof(RGBTRIPLE) * height * width);

    // Iterate over every row of the image
    for (int i = 0; i < height; i++)
    {
        // Iterate over every column of the image
        for (int j = 0; j < width; j++)
        {
            // start average counter at 0.0
            float average = 0.0;
            // start RGB values at 0
            int red = 0;
            int green = 0;
            int blue = 0;

            // Iterate over rows around current row
            for (int k = -1; k <= 1; k++)
            {
                // Iterate over columns around current column
                for (int l = -1; l <= 1; l++)
                {
                    // If current row + next row are within bounds
                    // If current column + next column are within bounds
                    if (i + k != height && i + k != -1 && j + l != width && j + l != -1)
                    {
                        // Update RGB values to the sum both pixel values
                        red += temp[i + k][j + l].rgbtRed;
                        green += temp[i + k][j + l].rgbtGreen;
                        blue += temp[i + k][j + l].rgbtBlue;
                        // Increment average by one for one pixel in the sum
                        average++;
                    }
                }
            }
            // Applying the calculated values
            image[i][j].rgbtRed = round(red / average);
            image[i][j].rgbtGreen = round(green / average);
            image[i][j].rgbtBlue = round(blue / average);
        }
    }
}

//Helper function to select minimum value
int min(int a, int b)
{
    if (a < b)
        return a;
    else
        return b;
}
