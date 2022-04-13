NAME=akhilsadam
PACKAGE=flask-redis
TAG=0.0.2
PYTEST=testall.py
APIFILE=doc/api.md
SEARCH=\\n
REPLACE=\n

rapid: kill clean build run

images:
	docker images | grep ${PACKAGE}

ps:
	docker ps -a | grep ${PACKAGE}

kill:
	- docker stop data-redis
	- docker stop ${PACKAGE}
clean:
	- docker rm data-redis
	- docker rm ${PACKAGE}
	- rm __pycache__/ -r
	- rm app/.pytest_cache/ -r

build:
	docker build -t ${NAME}/${PACKAGE}:${TAG} .

run:
	sh run.sh ${NAME} ${PACKAGE} ${TAG}

push:
	docker login docker.io
	docker push ${NAME}/${PACKAGE}:${TAG}


# [WARNING] The following commands may require unlisted dependencies and are not part of the supported API.
# Notes for developer convenience:
#	 May need to be done on Windows due to some npm issues.

api:
# container must be running!
	curl -X GET "http://localhost:5026/api/save" -H "accept: application/json" -o "${APIFILE}"

readme:
	git status
	npx @appnest/readme generate
	git status
	git add .
	- git commit -am "[auto] update readme"
	- git push

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
	make test
	make run 
	# run doc in a win terminal

doc:
	make api
	make readme