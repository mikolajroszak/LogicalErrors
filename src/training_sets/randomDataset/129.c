//#include <stdio.h>
main(int argc, char *argv[])
{
 int position;
 char buffer[133];
 FILE *fp;
 char *i;
 if (argc == 2)
 fp = fopen(argv[1], "r");
 else
 exit(1);
 if (fp == NULL)
 exit(1);
 while (!feof(fp)) /* this is a stupid thing to do in C! */
 {
 i = fgets(buffer, sizeof(buffer), fp);
 printf("%p: ", i);
 fputs(buffer, stdout);
 }
fclose(fp);
}
