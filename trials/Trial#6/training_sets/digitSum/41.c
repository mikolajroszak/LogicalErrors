//#include<stdio.h>
main()
{
	long int k;
	int sum=0,i;
	printf("enter the value of k");
	scanf("%ld",&k);
	lable:
	while(k>0)
    {
    	i=k%10;
    	sum=sum+i;
    	k=k/10;
    }
    if(sum>9)
    {
    	k=sum;
        sum=0;
        goto lable;
    }
    else
    {
    	printf("%d",sum);
    }
}          
       
       
 
 

       
  
 


