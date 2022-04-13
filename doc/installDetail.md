
The following commands are all terminal commands, and are expected to run on a Ubuntu 20.04 machine with Python3, and are written in that fashion. Mileage may vary for other systems. We will describe the Docker installation first.   

### From Docker:

#### Install

To install the Docker container, first install Docker.  

  - `apt-get install docker` (if using an Ubuntu machine, else get Docker from <a href="https://www.docker.com/">docker.com</a>.)  
  
Next install the containers.  

  - `docker pull akhilsadam/positional-iss:0.0.2`  

#### Run  

To test the code, please run the following in a terminal.  

  - `docker run -it --rm akhilsadam/positional-iss:0.0.2 testall.py`  


To run the code, please run the following in a terminal. The terminal should return a link, which can be viewed via a browser or with the `curl` commands documented in the API reference section.  

  - `docker run --name "positional-iss" -p 5026:5026 akhilsadam/positional-iss:0.0.2 wsgi.py`  


Now we will move to the source installation.  

### From Source:  

Since this is a Docker build, the requirements need not be installed on the server, as it will automatically be done on the Docker image.  
All commands, unless otherwise noted, are to be run in a terminal (in the home directory of the cloned repository).  

#### Build  

Again, first install Docker.  

  - `apt-get install docker` (if using an Ubuntu machine, else get Docker from <a href="https://www.docker.com/">docker.com</a>.)  
  
Next, clone the repository and change directory into the repository.  

  - `git clone git@github.com:akhilsadam/positional-iss.git`  

  - `cd positional-iss`  


Now build the image.  

  - `make build`  

#### Run  

To test the code, please run one of the following.  

  - `make test`  

  - `pytest`  


To run the code, please run the following. The terminal should return a link, which can be viewed via a browser or with the `curl` commands documented in the API reference section.  

  - `make run`  

To run a rebuild of the code, run this command instead. This command will automatically kill, rebuild, and test the code before running.  

  - `make iterate`  

