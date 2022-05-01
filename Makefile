# Make sure your variables are correct! (The TACC variable can be any username without ,_,-, or any other fancy characters.) 
# Note that you CAN run/deploy exactly as it is, but then my deployment and yours will fight each other (we will be starting/restarting the same kubernetes deployments.)

NAME=akhilsadam
TACC?=astacc

PACKAGE=compose
WORKER=compose-worker
GITHUB=git@github.com:akhilsadam/compose-dev.git
TAG=0.0.2
PYTEST=testall.py
APIFILE=doc/api.md
SEARCH=\\n
REPLACE=\n

TEST=test
PRODUCTION=production

nAPI=2
nWRK=3

# a full rebuild (we need so many variants due to the redis-url finding bash code..this can be optimized later)


iteratetest : kill clean build test

iterate: kill clean build run

###############

# kubernetes: (CAN PROBABLY be simplified)
cubecp:
	cp deployment/template/*.yml deployment/

cubereplT:
	bash scripts/repl-deploy.sh ${TACC} 1 ${TEST} ${PRODUCTION} 1 1

cuberepl:
	bash scripts/repl-deploy.sh ${TACC} 0 ${TEST} ${PRODUCTION} ${nAPI} ${nWRK}

cubeservicedeploy:
	kubectl apply -f deployment/service-flask.yml
	kubectl apply -f deployment/service-redis.yml

cubereplTdeploy:
	bash scripts/repl.sh ${TEST}

cuberepldeploy:
	bash scripts/repl.sh ${PRODUCTION}

cubedeploy:
	kubectl apply -f deployment/data-redis-volume.yml
	kubectl apply -f deployment/data-flask-volume.yml
	kubectl apply -f deployment/deployment-redis.yml
	kubectl apply -f deployment/deployment-worker.yml
	kubectl apply -f deployment/deployment-flask.yml
	kubectl apply -f deployment/service-nodeport.yml

cubecleanT: 
	- kubectl delete deployment compose-flask-${TEST}
	- kubectl delete deployment compose-worker-${TEST}
	- kubectl delete deployment compose-redis-${TEST}
	- kubectl delete pvc compose-data-redis-volume-${TEST}
	- kubectl delete pvc compose-data-flask-volume-${TEST}
	- kubectl delete services compose-flask-service-${TEST}
	- kubectl delete services compose-redis-service-${TEST}
	- kubectl delete services compose-nodeport-service-${TEST}

cubeclean:
	- kubectl delete deployment compose-flask-${PRODUCTION}
	- kubectl delete deployment compose-worker-${PRODUCTION}
	- kubectl delete deployment compose-redis-${PRODUCTION}
	- kubectl delete pvc compose-data-redis-volume-${PRODUCTION}
	- kubectl delete pvc compose-data-flask-volume-${PRODUCTION}
	- kubectl delete services compose-flask-service-${PRODUCTION}
	- kubectl delete services compose-redis-service-${PRODUCTION}
	- kubectl delete services compose-nodeport-service-${PRODUCTION}

cubewipe:
	- rm deployment/*.yml

cubeiterateT: cubecleanT cubecp cubereplT cubeservicedeploy cubereplTdeploy cubedeploy cubewipe cubes# Test
cubeiterate: cubeclean cubecp cuberepl cubeservicedeploy cuberepldeploy cubedeploy cubewipe cubes# Deploy

cubes:
	kubectl get pods
	kubectl get deployments
	kubectl get pvc
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
	- rm flask-data/*.mp3
	- rm flask-data/*.mid
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