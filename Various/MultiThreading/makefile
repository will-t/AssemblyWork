test=primes
test1=primes3.txt
compile=-Wall -g -pthread -o
param=1 primes3.txt
make:primesexe
primesexe:primes.cpp
	g++ $(compile) primeexe primes.cpp
run:
	$(shell echo bash ./run.sh )
clean:
	rm $(test1) $(test)
