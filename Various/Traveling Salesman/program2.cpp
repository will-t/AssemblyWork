/*
     Title: Traveling Salesman Problem     
     Author: William Turner III
     Date: 4/11/2022     
     Purpose:   Traveling Salesman - find the lowest cost
                tour when traveling from US to 8 other countries
                and then back to US.
*/

#include <iostream>
#include <fstream>
#include <cmath>
#include "GraphMatrix.h"
using namespace std;
int sumtot = 0;
const int SIZE = 10;
const string COUNTRY_CODES[SIZE]={"AU", "BR", "CA", "CN", "GL", "IT", "NA", "RU", "US", "US"};
struct Tour
{
	string tour[SIZE];
	int cost =0;
};
//Function Prototypes 
GraphMatrix* readFileMakeMatrix();
void printStringArray(string* arr, int size);
void lexicographic(string param[], int size, Tour *tour, GraphMatrix *matrix); 
int searchCountryCode(string country);
void saveTour(string *param, Tour *tourOptions, GraphMatrix *matrix);
int getWeight(int v1, int v2);
void findLowest(Tour *tour);
int main()
{	
	Tour *tourOptions = new Tour[40320]; //this is my array for tours 
	//read in the flight information from the file and then create the weight matrix
	GraphMatrix * matrix = readFileMakeMatrix();
	string * countries = new string[SIZE-2];
	
	cout << "\n\n*************************COUNTRIES*******************\n";
	for(int x=0; x < SIZE-2; x++)
	{
		countries[x] = COUNTRY_CODES[x];
		cout << countries[x] << endl;
	}
	//call lexicographic to find the permutations of the countries
	lexicographic(countries, SIZE-2, tourOptions,matrix);
	cout << "\n\n*************************SOLUTION*******************\n";

	cout << "\nHappy Traveling!\n";

	//free up memory allocated for tourOptions
	//get rid of tourOptions when done
	findLowest(tourOptions);
	delete[] tourOptions;
	return 0;
}

int searchCountryCode(string country)
 { //searchCountryCode using search algorithm specified in the assignment
	 int low = 0;
	 int high = SIZE-1;
	 int mid = 0;
	 
	 while(low <= high)
	 {
		 mid = (low + high)/2;
		 if(COUNTRY_CODES[mid] == country)
		 {
			 return mid;
		 }
		 else if(COUNTRY_CODES[mid] < country)
		 {
			 low = mid + 1;
		 }
		 else
		 {
			 high = mid - 1;
		 }
	 }
	 return -1; 
 }

GraphMatrix* readFileMakeMatrix()
{
	ifstream inFile;
	GraphMatrix * matrix = new GraphMatrix(SIZE-1);
	cout << "\nCreated the matrix.";
	string country1, country2;
	int price;
	inFile.open("flights.txt");
	cout << "\nReading from flights.txt\n";
	if(inFile)
	{
		while(inFile >> country1)
		{
			inFile >> country2;
			inFile >> price;
			//add price to graph matrix
			matrix->addEdge(searchCountryCode(country1), searchCountryCode(country2), price);
			cout << "\nAdded edge from " << country1 << " to " << country2 << " with cost of $" << price;
		}
	}
	else
		cout << "\nSorry, I am unable to open the file.\n";
	inFile.close();
	cout << "\n\nFLIGHT PRICE GRAPH MATRIX\n";
	matrix->printGraph();
	cout << endl;
	return matrix;
}

/*
	Title: printStringArray
	Purpose:  this function will print the array of strings with a space
		between each string
*/
void printStringArray(string* arr, int size)
{
	for(int x=0; x<size; x++)
	{
		cout << arr[x] << " "; //simple printout for an array passing in size and array
	}
	cout << endl;
}




void lexicographic(string *param, int size, Tour *tourOptions, GraphMatrix *matrix )
{
	string tempString[size];
	for(int i = 0; i < size; i++)
	{
		tempString[i] = param[i];
	}
	 
	bool isDone = false;
	int iterationCount = 1;
	int lowBound = 0;		//The "i" value
	int uppBound = 0;		//The "j" value
	
	//Temporary variables to store values during a swap
	string tempChar;
	string swapString;
	string tempArray[size];
	cout << "\nLEXICOGRAPHIC ALGORITHM";
	
	while(!isDone)
	{

		cout << "\nIteration " << iterationCount << ": ";
		printStringArray(tempString, size);
		cout << "\n" << iterationCount << ":\t";
		iterationCount++;

		isDone = true;
		for(int i = 0; i < size-1; i++)
		{
			if(tempString[i]<tempString[i+1])
			{
				isDone = false;
				lowBound = i;
			}
		}
		if(isDone)
			continue;
		/*
			---FIND uppBound---
		*/
		for(int j = size-1; j>0; j--)
		{
			if(tempString[j] > tempString[lowBound])
			{
				uppBound = j;
				break;
			}
		}
		/*
			---SWAP ELEMENTS---
		*/
		tempArray[lowBound] = tempString[lowBound];
		tempString[lowBound] = tempString[uppBound];
		tempString[uppBound] = tempArray[lowBound];
		for(int i = 1;i < size-lowBound;i++)
		{
			tempArray[lowBound+i] = tempString[size-i];
		}
		for(int i = 1;i < size-lowBound;i++)
		{
			tempString[lowBound+i] = tempArray[lowBound+i];
		}
		/*
			---PRINT lowBound AND uppBound---
		*/
		
		
	   saveTour(tempString, tourOptions, matrix); //send options to saveTour
	   sumtot++; //increase counter for index inside saveTour
	}
	
	cout << "\nLexicographic Algorithm complete!";
}

void saveTour(string *param, Tour *tourOptions, GraphMatrix *matrix)
{	//appending US to the front and end of the array by creating a buffer array with 2 more elements 
	string ffString[10];
	ffString[0] = "US";
	ffString[1] = param[0];
	ffString[2] = param[1];
	ffString[3] = param[2];
	ffString[4] = param[3];
	ffString[5] = param[4];
	ffString[6] = param[5];
	ffString[7] = param[6];
	ffString[8] = param[7];
	ffString[9] = "US";
	cout << "\n";
	printStringArray(ffString, 10);
	cout << "\n";
	int cost =0;
	for(int i = 0; i < 9; i++) //9?
	{
		cost += matrix->getWeight(searchCountryCode(ffString[i]), searchCountryCode(ffString[i+1]));
		//parsing through the array getting various index and geting the cost from getweight in matrix then adding it to cost
	}
	
	tourOptions[sumtot].cost = cost; //adding cost to associated tour struct
	for(int i = 0; i < 10; i++)
	{
		tourOptions[sumtot].tour[i] = ffString[i]; //adding elements to the tour array
	}
	//cout << "\nTour: ";
	cout << "\nCost: $" << cost;
	return;
}

void findLowest(Tour *tourOptions)
	{
	//search through the tour array to find the lowest cost and print it

	int lowestBuf = 0;
	int indexHold = 0;
	for(int i = 0; i < 40319; i++){
		if(i == 0)
		{
			lowestBuf = tourOptions[i].cost;
			
		}
		else
			{
				if(tourOptions[i].cost < lowestBuf){
					lowestBuf = tourOptions[i].cost;
					indexHold = i;
				}

			}
		
		}
	cout << "\nLowest cost: $" << lowestBuf;
	
	for(int i = 0; i < 10; i++)
		cout << " " <<tourOptions[indexHold].tour[i] ;
	cout << endl;
	return;

}
