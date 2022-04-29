id=`docker run -d -p 6426:6379 -v "${PWD}/redis-data:/data:rw" --name=data-redis redis:6 --save 1 1`
echo $id
ipa=`docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "${id}"`
echo $ipa
docker run --name "$2" -v "${PWD}/flask-data:/app/app/static/audio:rw" -p 5026:5026 $1/$2:$3 core.py $ipa work &
docker run --name "$4" -v "${PWD}/flask-data:/app/app/static/audio:rw" $1/$4:$3 worker.py $ipa && fg