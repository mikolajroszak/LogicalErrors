
//#include <stdio.h>

//#include <string.h>

 

#define SIZE 50

 

void main()

{

    char string[SIZE], string1[SIZE], string2[SIZE];

    int i, j = 0, a = 0, temp, len = 0, len1 = 0, k = 0;

 

    printf("\nEnter a string:");

    scanf("%[^\n]s", string1);

 

    /* Code to remove whitespaces */

    for (i = 0;string1[i] != '\0';i++)

    {    

        if (string1[i] == ' ')

        {

            continue;

        }

        string[j++] = string1[i];

    }

 

    /* Code to sort the string */

    for (i = 0;string[i] != '\0';i++)

    {

        for (j = i + 1;string[j] != '\0';j++)

        {

            if (string[i] > string[j])

            {

                temp = string[i];

                string[i] = string[j];

                string[j] = temp;

            }

        }

    }

    string[i] = '\0';

    len = strlen(string);

 

    /* Code to remove redundant characters */

    for (i = 0;string[i] != '\0';i++)

    {

        if (string[i] == string[i + 1] && string[i + 1] != '\0')

        {

            k++;

            continue;

        }

        string2[a++] = string[i];

        string[a] = '\0';

    }

    len1 = len - k;

    printf("The sorted string is:");

    for (temp = 0;temp < len1;temp++)

    {

        printf("%c", string2[temp]);

    }

}
