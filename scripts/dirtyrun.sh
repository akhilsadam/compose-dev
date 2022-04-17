id=`docker run -d -p 6426:6379 -v "${PWD}/redis-data:/data:rw" --name=data-redis redis:6 --save 1 1`
echo $id
ipa=`docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "${id}"`
echo $ipa

echo $PWD
docker run -it -v "${PWD}/:/app/" --name "$2" -p 5026:5026 $1/$2:$3 core.py $ipa