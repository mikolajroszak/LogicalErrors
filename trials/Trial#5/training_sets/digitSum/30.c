//#include<stdio.h>
void main()
{
	long int n;
	int sum=0,rem;
	printf("\n enter the number");
	scanf("%ld",&n);
	l:
	while(n!=0)
	{
		rem=n%10;
		sum+=rem;
		n=n/10;
	}
	if(sum<10) 	
		printf("sum=%d",sum);
	else
	{
		n=sum;
		sum=0;
		goto l;
	}
}
