#/bin/bash
x=20
while [ $x -lt 41 ]
do
r=$((x * 1000)) 
amountcount=0
for ((i = 0; i < 19; i++))
do
./part1 $r >> numbers.csv
done
((x++))
done
filename="numbers.csv"
lines=$(cat $filename)
for line in $lines  
do  
test1=${line//[A-Za-z\:]/} 
echo $test1 >> test1.csv
sed -i '/^$/d' test1.csv 
done
AverageTime=0.0
LoopCounter=0
counterinfo=20
while IFS= read -r line
do
AverageTime=$(echo "scale=10;($AverageTime + $line)" | bc)
AverageTime2=$(echo "scale=10;($AverageTime / 20)" | bc)
((LoopCounter++))

if [ $LoopCounter -eq 19 ] 
then
L=$((counterinfo * 1000))
 echo "$L    $AverageTime2" >> FinalNums.csv
let counterinfo++
AverageTime=0
LoopCounter=0
fi
done < test1.csv

