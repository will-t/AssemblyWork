#include <iostream>
#include <threads.h>
#include <cstdlib>
#include <cstdio>
#include <atomic>
#include <vector>
#include <algorithm>
#include <string.h>
bool is_prime_slow(int n);
void doprimes(int id);
std::atomic<int> count(0);
//create global number vector to store numbers from a file
std::vector<int> numbers;
int thread_number;

//read primes_file.txt and store numbers in vector
//create global thread number to store amount of threads to be used

//take in two arguments from command line and the amount 
int main(int argc, char** argv){
printf("Enter the amount of threads to be used followed by the file name\n");
//read the file they have given to the numbers vector
 FILE *fp;
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    fp = fopen(argv[2], "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);
    while ((read = getline(&line, &len, fp)) != -1) {
        numbers.push_back(atoi(line));
        
    }
 fclose(fp);
//finished reading numbers into vector

//get the amount of threads provided by cmd line converted 
thread_number = atoi(argv[1]);

   thrd_t threads[thread_number];
if(thread_number > 1 && thread_number < 9){
    for(int i = 0; i < thread_number; i++){
        //thrd_create(&threads[i], &doprimes, (void*)i);
        thrd_create(&threads[i], (thrd_start_t) doprimes, (void *) (long) i);
    }
    for(int i = 0; i < thread_number; i++){
        thrd_join(threads[i], NULL);
    }
    std::cout<< "\n" <<count << "\n";
}else if (thread_number == 1){
    thrd_create(&threads[0], (thrd_start_t) doprimes, (void *) (long) 0);
    thrd_join(threads[0], NULL);
    std::cout << "\n" << count;
}else{
    printf("Incorrect Thread Number try a range of 1-8");
}
    
    }


bool is_prime_slow(int n) {
    if (n == 2 || n == 3)
        return true;

    for (int i = 2; i * 2 <= n; i++) {
        if (n % i == 0)
            return false;
    }

    return true;
}


void doprimes(int id){
    //set chunk_size to nums_vector size divided by number of threads
 
    int test = numbers.size(); //18000
    int chunk_size = test/thread_number; //4
    int start = id * chunk_size;
    int test1 = start + chunk_size;
    int end = std::min(test1, test);
    for(int i = start; i < end; i++){
        if(is_prime_slow(numbers[i]) == true){
            count = count+1;
        
        }

    }
    return;
}