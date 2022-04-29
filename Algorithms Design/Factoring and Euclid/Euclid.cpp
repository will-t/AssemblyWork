/*
William Turner
CSC 2400 01
*/
#include <iostream>
#include <cstdlib>
using namespace std;
int euc(int a, int b);
// Setting up a function to call later designated to be Euclids Algorithm
int main(int argc, char* argv[])
{
    /*
    If the amount of arguments is not 3 the program will terminate and give them the correct command usage
    */
if(argc !=3){
    cout << "Incorrect useage of execuatable use this command m being the larger number n being the smaller, ./file m n";
}
    /*
    This if statement checks if the number the provided are equal to zero after being converted to number the computer can read using the atoi library
    */
if(atoi(argv[1]) == 0 || atoi(argv[2]) == 0){
    cout << "Gcd is undefined";
}
    /*
    Finally if the amount of arguments are correct we will begin by storing the converted numbers in some place holders I created
    After that I call the function Euc with the variables provided by the user m and n
    */
if(argc == 3){
    int num1 = atoi(argv[1]); 
    int num2 = atoi(argv[2]);
    int test = euc(num1, num2);
    cout <<"Gcd (" << atoi(argv[1]) << ", " << atoi(argv[2]) << ") is " << test ;
    }
}
int euc(int num1, int num2){
    int num3;
    //setup a variable num3 to use as needed throughout calculations
    while ((num1 % num2)!= 0){
    //as long as the mod of num1 and num2 it will continute running this loop
        cout << "Gcd (" << num1 << ", " << num2 << ")" << "\n" ;
             
        num3 = num1 % num2;
    //used the buffer I created to store the remained of num1 and num2
        num1 = num2;
    //set num1 to the place of num2
        num2 = num3;
    //set num2 equal to the variables stored in the buffer
}
return num2;
}



/*ignore test couts
 cout << "Gcd (" << num2 << "," << "(" << num1 << "%" << num2 << "))" << "\n"; 
 cout << "Gcd(" << num3 << "," << num1 << "%" << num2 << "))" << "\n";  
*/