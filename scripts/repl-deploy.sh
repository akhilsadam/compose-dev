#!/bin/bash
cd ../deployment
cat ~/portinfo
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