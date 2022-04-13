NAME=akhilsadam
PACKAGE=compose
GITHUB=git@github.com:akhilsadam/compose-dev.git
TAG=0.0.2
PYTEST=testall.py
APIFILE=doc/api.md
SEARCH=\\n
REPLACE=\n

# cheap versions that do not rebuild the complete image (dirty stands for an 'unclean' build)

rapid: kill clean dirtyrun

rapidtest: kill clean dirtytest

# a full rebuild (we need so many variants due to the redis-url finding bash code..this can be optimized later)

iteraterun : kill clean build run

iteratetest : kill clean build test

iterate: kill clean build testrun

###############

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
	- rm doc/r/log_r.txt

build:
	docker build -t ${NAME}/${PACKAGE}:${TAG} .

dirtytest:
# only test (without rebuild)
	sh scripts/dirtytest.sh ${NAME} ${PACKAGE} ${TAG}

dirtyrun:
# only run (without rebuild)
	sh scripts/dirtyrun.sh ${NAME} ${PACKAGE} ${TAG}

test:
# only test
	sh scripts/test.sh ${NAME} ${PACKAGE} ${TAG}

run:
# only run
	sh scripts/run.sh ${NAME} ${PACKAGE} ${TAG}

testrun:
# test and run
	sh scripts/run.sh ${NAME} ${PACKAGE} ${TAG}

push:
	docker login docker.io
	docker push ${NAME}/${PACKAGE}:${TAG}


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