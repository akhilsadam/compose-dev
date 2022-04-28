NAME?=akhilsadam
TACC?=as_tacc
PACKAGE=compose
WORKER=compose-worker
GITHUB=git@github.com:akhilsadam/compose-dev.git
TAG=0.0.2
PYTEST=testall.py
APIFILE=doc/api.md
SEARCH=\\n
REPLACE=\n

# a full rebuild (we need so many variants due to the redis-url finding bash code..this can be optimized later)

iteraterun : kill clean build run

iteratetest : kill clean build test

iterate: kill clean build testrun

###############

# kubernetes:
cubecp:
	cp deployment/template/*.yml deployment/
	bash scripts/repl-user.sh

cubereplT:
	bash scripts/repl-deploy.sh ${USERNAME} ${ID} test

cuberepl:
	bash scripts/repl-deploy.sh ${USERNAME} ${ID} deploy

cubedeploy:
	bash scripts/repl.sh
	kubectl apply -f deployment/service-flask.yml
	kubectl apply -f deployment/service-redis.yml
	kubectl apply -f deployment/service-worker.yml
	kubectl apply -f deployment/data-redis-volume.yml
	kubectl apply -f deployment/data-flask-volume.yml
	kubectl apply -f deployment/deployment-redis.yml
	kubectl apply -f deployment/deployment-worker.yml
	kubectl apply -f deployment/deployment-flask.yml
	kubectl apply -f deployment/service-nodeport.yml

cubecleanT: 
	- kubectl delete deployment compose-flask-test
	- kubectl delete deployment compose-worker-test
	- kubectl delete deployment compose-redis-test
	- kubectl delete pvc compose-data-redis-volume-test
	- kubectl delete pvc compose-data-flask-volume-test
	- kubectl delete services compose-flask-service-test
	- kubectl delete services compose-worker-service-test
	- kubectl delete services compose-redis-service-test
	- kubectl delete services compose-nodeport-service-test

cubeclean:
	- kubectl delete deployment compose-flask
	- kubectl delete deployment compose-worker
	- kubectl delete deployment compose-redis
	- kubectl delete pvc compose-data-redis-volume
	- kubectl delete pvc compose-data-flask-volume
	- kubectl delete services compose-flask-service
	- kubectl delete services compose-worker-service
	- kubectl delete services compose-redis-service
	- kubectl delete services compose-nodeport-service

cubewipe:
	- rm deployment/*.yml

cubeiterateT: cubecleanT cubecp cubereplT cubedeploy cubewipe # Test
cubeiterate: cubeclean cubecp cuberepl cubedeploy cubewipe # Deploy
###############

images:
	docker images | grep ${PACKAGE}
	docker images | grep ${WORKER}

ps:
	docker ps -a | grep ${PACKAGE}
	docker ps -a | grep ${WORKER}

kill:
	- docker stop data-redis
	- docker stop ${PACKAGE}
	- docker stop ${WORKER}
	- docker stop ${PACKAGE}-test
clean:
	- docker rm data-redis
	- docker rm ${PACKAGE}
	- docker rm ${WORKER}
	- docker rm ${PACKAGE}-test
	- rm __pycache__/ -r
	- rm app/__pycache__/ -r
	- rm app/api/__pycache__/ -r
	- rm app/core/__pycache__/ -r
	- rm app/quarry/__pycache__/ -r
	- rm app/queue/__pycache__/ -r
	- rm app/shaft/__pycache__/ -r
	- rm app/.pytest_cache/ -r
	- rm doc/r/log_r.txt
	- rm redis-data/dump.rdb

build:
	docker build -t ${NAME}/${PACKAGE}:${TAG} -f docker/Dockerfile.api .
	docker build -t ${NAME}/${WORKER}:${TAG} -f docker/Dockerfile.wrk .

test:
# only test
	sh scripts/test.sh ${NAME} ${PACKAGE} ${TAG} ${WORKER}

run:
# only run
	sh scripts/run.sh ${NAME} ${PACKAGE} ${TAG} ${WORKER}

testrun:
# test and run
	sh scripts/testrun.sh ${NAME} ${PACKAGE} ${TAG} ${WORKER}

push:
	docker login docker.io
	docker push ${NAME}/${PACKAGE}:${TAG}
	docker push ${NAME}/${WORKER}:${TAG}


# [WARNING] The following commands may require unlisted dependencies and are not part of the supported API.
# Notes for developer convenience:
#	 May need to be done on superuser Windows due to some R issues.
#	 Requires R and some packages
#	 Some paths will need to be modified (currently designed for @akhilsadam to run, but if you would like to do it too, please let me know).

api:
# containers must be running!
	curl -X GET "http://localhost:5026/api/save" -H "accept: application/json" -o "${APIFILE}"

readme:
	git status
	npx @appnest/readme generate
	git status
	git add .
	- git commit -am "[auto] update readme"
	- git push

pdf:
	"C:\Program Files\R\R-4.0.3\bin\Rscript" -e 'install.packages('"'pagedown'"', repos = '"'http://cran.us.r-project.org'"')' > doc/r/log_r.txt
	"C:\Program Files\R\R-4.0.3\bin\Rscript" -e 'pagedown::chrome_print('"'doc/r/article.rmd'"')' > doc/r/log_r.txt
# sudo "/mnt/c/Program Files/R/R-4.0.3/bin/Rscript.exe" -e 'install.packages('"'pagedown'"')' > doc/r/log_r.txt
# "/mnt/c/Program Files/R/R-4.0.3/bin/Rscript.exe" -e 'pagedown::chrome_print('"'doc/r/article.rmd'"')' > doc/r/log_r.txt
	mv doc/r/article.pdf app/static/doc/article.pdf
	mv doc/r/article.html app/static/doc/article.html

commit:
	git status
	git add .
	git commit -am "[glob] ${msg}"
	git push

all: 
	pytest 
	make kill 
	make clean 
	make build
	make testrun
	# run doc in a win terminal

doc:
	make api
	make pdf
	make readme

cleanport:
	lsof -i:5026

mildpurge: 
	docker rm `docker ps -qa`
	docker rmi `docker images -q`

purge:
# run on windows Powershell
	- docker system prune
	- net stop com.docker.service
	- wsl --shutdown
	"Optimize-VHD -Path C:\Users\sadam\AppData\Local\Docker\wsl\data\ext4.vhdx -Mode Full"