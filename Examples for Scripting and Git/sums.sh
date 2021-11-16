#/bin/bash
#IFS= ,
while IFS=', ' read -r num1 num2
do
	
	echo "Sums: $((num1 + num2))"
	
done < nums.csv
