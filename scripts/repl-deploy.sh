#!/bin/bash
pi=`cat ~/portinfo`
echo "------------"
echo "$pi"
echo "------------"
lines=($(echo $(echo "$pi" | awk -F: '{print $2}')))
linesA=($(echo $(echo "$pi" | awk -F: '{print $3}')))
if test $2 -gt 0
then
    np=${lines[2]}
    npa=$(echo ${lines[4]}${linesA[1]} | tr -d '"')
    env=test
else
    np=${lines[1]}
    npa=$(echo ${lines[3]}${linesA[0]} | tr -d '"')
    env=production
fi

echo "environment: $env | @ip_address: $npa | with port: $np"

cd $(pwd)/deployment/
for f in $(echo *)
do
    if [ -f "$f" ]
    then
        echo "Processing $f file..."
        firstString=$(<$f)
        firstString=$(echo "${firstString//NODEPORT/"$np"}")
        firstString=$(echo "${firstString//ENVSTYLE/$env}")
        echo "${firstString//USERNAME/"$1"}" > $f
    fi
done

# firstString=$(<deployment-flask.yml)
# firstStringTwo=$(<deployment-worker.yml)
# secondString=$(echo $(kubectl get services compose-redis-service --output=jsonpath="{.spec.clusterIP}") | tr -d '"')
# echo $secondString
# repline=$(echo "${firstString/ip_address/"$secondString"}")
# echo "$repline"   
# echo "$repline" > deployment-flask.yml
# repline=$(echo "${firstStringTwo/ip_address/"$secondString"}")
# echo "$repline"   
# echo "$repline" > deployment-worker.yml