#!/bin/bash
cd ../
pi=`cat ~/portinfo`
echo "$pi"
lines=($(echo $(echo "$pi" | awk -F: '{print $2}')))

if test $2 -gt 0
then
    np=${lines[2]}
    env=test
else
    np=${lines[1]}
    env=production
fi

echo $np

FILES="deployment/*"
for f in $FILES
do
  echo "Processing $f file..."
  firstString=$(<$f)
  firstString=$(echo "${firstString/NODEPORT/"$np"}")
  firstString=$(echo "${firstString/ENVSTYLE/"$env"}")
  echo "${firstString/USERNAME/"$1"}" > $f
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