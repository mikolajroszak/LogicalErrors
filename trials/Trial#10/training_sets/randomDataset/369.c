
//#include <stdio.h>

#define NUM_BITS_INT sizeof(int)*8

 

void main()

{

    unsigned int number;

    int i = 0, hexadecimal, rev = 0, bit;

 

    printf("enter the hexdecimal value\n");

    scanf("0x%number", &hexadecimal);

    while (i++ < NUM_BITS_INT)

    {

        bit = hexadecimal & 1;

        hexadecimal = hexadecimal >> 1;

        rev = rev ^ bit;

        if (i < NUM_BITS_INT)

            rev = rev << 1;

    }

    printf("reverse of hexadecimal value is 0x%number", rev);

}
