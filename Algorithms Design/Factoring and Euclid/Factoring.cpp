/*
William Turner
CSC 2400 01
*/

#include <iostream>
#include <cstdlib>
using namespace std;
int cic(int a, int b);
/*
Setting up the cic function to where I can specify two variables and call the function later in the program.
*/
int main(int argc, char* argv[])
{
/*
If the amount of arguments is not 3 the program will terminate and give them the correct command usage
*/
if(argc !=3){
    cout << "Incorrect useage of execuatable use this command m being the larger number n being the smaller, ./file m n \n";
    return 0;
}
/*
This if statement checks if the number the provided are equal to zero after being converted to number the computer can read using the atoi library
*/
if(atoi(argv[1]) == 0 || atoi(argv[2]) == 0){
    cout << "Gcd is undefined";
    return 0;
}
/*
Finally if the amount of arguments are correct we will begin by storing the converted numbers in some place holders I created
After that I call the function cic with the variables provided by the user m and n
*/
if(argc == 3){
    int m = atoi(argv[1]); 
    int n = atoi(argv[2]);
    int answ = cic(m, n);
    //cout << answ ;
    }
}
int cic(int m, int n){
    // setup the variable t which is equal to the smaller of the two numbers 
    int t = n;
    while(t !=0){
        // if t is not zero it will continute otherwise it will return
         int res1 = m % t;
        /* 
        takes the mod of m and t storing in the variable res1
        Then will check if res1 is either 0 and if so will start on the second number 
        otherwise it will continute the loop to find a remainder of 0
        */
        if(res1 != 0){
            cout <<"Gcd("<< m << ","<< t << ")" << "= " << res1;
            cout << "\n";
             t--;
        }
        
         if(res1 == 0){
             cout << "checked n: gcd(" << m << "," << t << ")" << "is ";
             int res2 = n % t;
             if(res2 != 0){
                 cout << res2;
                 cout << "\n";
                 t--;
        /*
        Preforms the same actions as above for res1 on a second number res2 to find the answer for the second variable provided.
        Will either loop or execute depending on what the mod operator returns
        */
             }
             if(res2 == 0){
                 cout << t << "\n";
                 cout << "The Gcd(" << m << "," << n << ") is " << t;
                 return 0;
             }
            
             
             
             
         }
       
        
            

        
    }
    
        }