//#include <stdio.h>
//#include <stdlib.h>
main( int argc, char *argv[] )
{
 int ch, chlower;
 FILE *fpin;
 switch (argc) /* check number of arguments */
 {
 /* one argument - file not specified, so input from stdin */
 case 1: fpin = stdin;
 break;
 /* two arguments - open specified file and check to see if it exists */
 case 2: fpin = fopen(argv[1], "r");
 if (fpin == NULL)
 {
 fprintf(stderr, "%s: file not found\n", argv[1]);
 exit(1);
 }
 break;
 /* three or more arguments - report error condition */
 default:
 fprintf(stderr, "%s: too many arguments\n", argv[0]);
 exit(1);
 }
 /* read in the characters in the file */
 while ( (ch = getc(fpin)) != EOF )
 {
 chlower = ch | 0x20; /* fast convert to lower case for testing purposes - can get */
 /* away with this as the original value is unchanged... */
 if ((chlower >= 'a') && (chlower <= 'm')) /* so now only 2 comparisons are needed */
 ch += 13;
 if ((chlower >= 'n') && (chlower <= 'z'))
 ch -= 13;
 putc(ch, stdout); /* print out the character to the standard output */
 }
 fclose(fpin);
 exit(0);
}
