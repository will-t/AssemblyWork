#/bin/bash
x=1
thread=2
while [ $x -lt 21 ]
do
r=$((x))
amountcount=0
for ((i = 0; i < 10; i++))
do
./part3 $thread $r >> numbers.csv
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
counterinfo=1
while IFS= read -r line
do
AverageTime=$(echo "scale=10;($AverageTime + $line)" | bc)
AverageTime2=$(echo "scale=10;($AverageTime / 11)" | bc)
((LoopCounter++))

if [ $LoopCounter -eq 10 ]
then
L=$((counterinfo))
 echo "$L $AverageTime2" >> FinalSums.csv
let counterinfo++
AverageTime=0.0
LoopCounter=0
fi
done < test1.csv



