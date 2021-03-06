id=`docker run -d -p $7:6379 -v "${PWD}/redis-data:/data:rw" --name=$5-data-redis redis:6 --save 1 1`
echo $id
ipa=`docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "${id}"`
echo $ipa
docker run --name "$5-$2" -v "${PWD}/flask-data:/app/app/static/audio:rw" -p $6:5026 $1/$2:$3 core.py $ipa &
docker run --name "$5-$4" -v "${PWD}/flask-data:/app/app/static/audio:rw" $1/$4:$3 worker.py $ipa && fg