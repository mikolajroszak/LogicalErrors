//#include<stdio.h>
//#include<math.h>
 
int main() {
   int side;
   float area, r_4;
 
   r_4 = sqrt(3) / 4;
 
   printf("\nEnter the Length of Side : ");
   scanf("%d", &side);
 
   area = r_4 * side * side;
 
   printf("\nArea of Equilateral Triangle : %f", area);
   return (0);
}
