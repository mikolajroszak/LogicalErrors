//#include<stdio.h>
 
void main() {
   int i = 0;
   char ch;
 
   for (i = 0; i < 256; i++) {
      printf("%c ", ch);
      ch = ch + 1;
   }
}
