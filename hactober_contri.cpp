#include <bits/stdc++.h> 
using namespace std; 
int main()
{
    int T;
    cin>>T;
    while(T--)
    {
     	int N,Q;
     	cin>>N>>Q;	
   		int a,b=0;				// initial floor, floor of request
   		long int sum=0;			
   		for(int i=0;i<Q;i++)
   		{
   		   cin>>a;
		   sum=sum+abs(a-b);
		   cin>>b;
		   sum=sum+abs(a-b);	
		}
	cout<<sum<<endl;
	} 	
}

