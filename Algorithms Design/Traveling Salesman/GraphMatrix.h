/*
	Title:  	GraphMatrix.h
	Author:		April R. Crockett
	Date:		February 24, 2022
	Purpose:	Adjacency matrix for representing a graph
*/

#ifndef GRAPHMATRIX_H
#define GRAPHMATRIX_H

#include <iostream>
#include <climits>
using namespace std;

class GraphMatrix
{
	private:
		int ** vertexMatrix;  //the matrix
		int numVertices;
		int numEdges;
		
	public:
		//constructor for creating the matrix with a given number of vertices
		GraphMatrix(int numV)
		{
			numVertices = numV;
			numEdges = 0;
			vertexMatrix = new int*[numV];
			
			for(int i=0; i<numVertices; i++)
			{
				vertexMatrix[i] = new int[numVertices];
			}
			
			for(int i=0; i<numVertices; i++)
			{
				for(int j=0; j<numVertices; j++)
					vertexMatrix[i][j] = 0; //set all elements to zero until we know that there is an edge
			}
		}
		
		//destructor to release all dynamically allocated arrays and array elements
		~GraphMatrix()
		{
			for(int i=0; i<numVertices; i++)
			{
				delete[] vertexMatrix[i];
			}
			delete[] vertexMatrix;	
		}
		
		/*
			Function addEdge()
			Input:  two vertices, which are integers where v1 has a directed edge toward v2
			Returns: none
			Purpose:  to create an edge between v1 to v2
		*/
		void addEdge(int v1, int v2, int value)
		{
			if(vertexMatrix[v1][v2] == 0) //no edge created yet
				numEdges++;
			vertexMatrix[v1][v2] = value;
			vertexMatrix[v2][v1] = value;
		}
		/*
			Function delEdge()
			Input: two vertices, which are integers where v1 has a directed edge toward v2
			Returns: none
			Purpose: to delete the edge
		*/
		void delEdge(int v1, int v2)
		{
			if(vertexMatrix[v1][v2] != 0)
				numEdges--;
			vertexMatrix[v1][v2] = 0;
		}
		
		/*
			Function printGraph()
			Input: none
			Returns: none 
			Purpose: to print the matrix
		*/
		void printGraph()
		{
			cout << endl;
			for(int i=0; i<numVertices; i++)
			{
				for(int j=0; j<numVertices; j++)
				{
					if(vertexMatrix[i][j] != INT_MAX)
						cout << vertexMatrix[i][j];
					else
						cout << "I";
					cout << "\t";
				}
				cout << endl;
			}
		}
		
		/*
			Function getWeight()
			Input: two vertices, which are integers
			Returns: the weight of the edge between v1 & v2
			Purpose: return the weight of the graph edge between v1 & v2
		*/
		int getWeight(int v1, int v2)
		{
			return vertexMatrix[v1][v2];
		}
};

#endif