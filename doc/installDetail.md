
The following commands are all terminal commands, and are expected to run on a Ubuntu 20.04 machine with Python3, and are written in that fashion. Mileage may vary for other systems.   

### From Source:  

Clone the repository and then use the makefile to start the containers (make sure Docker has been installed prior).   
`git clone https://github.com/akhilsadam/compose-dev`    
`cd compose-dev`    
`make iterate`    

Now either use a browser or a curl utility to interact with the application at `https://localhost:5026/`. Further instructions are provided in the API documentation below, and in the writeup, so please refer there as necessary.  

To perform integration tests, once the `make iterate` command has been run, in another terminal, type the following:  
`pytest`  
If no errors can be seen in terminal output, the application has passed the integration tests.    

### Kubernetes Deployment:    

Prerequisites: Create your public urls and ports, and place them in the `home` directory in a file called `portinfo`. The style should be as follows:  
```
docker port: 5026
kube port 1: 30026
kube port 2: 30126
public url 1: "https://isp-proxy.tacc.utexas.edu/as_tacc-1/"
public url 2: "https://isp-proxy.tacc.utexas.edu/as_tacc-2/"
```
Here we have given the ports as expected for the primary deployment cluster.  

Navigate to your preconfigured Kubernetes cluster via terminal, and then run the following commands in the terminal.  
`git clone https://github.com/akhilsadam/compose-dev`    
`cd compose-dev`   
`make cubeiterateT`  

If you are deploying to production, do `make cubeiterate` instead of `make cubeiterateT`.  

The Kubernetes services, PVCs, deployments, and pods should now be up and running.  

Note we do not perform integration tests on the Kubernetes cluster, however; if that is necessary, please tweak the `/test/test_api.py` file with the following replacement.  
`'http://localhost:5026/api/save'` -> `<your public url with proxy>/api/save`  
Now running `pytest` in the terminal should test the application.  

### From Docker  

As before, in a terminal, do the following:  
`git clone https://github.com/akhilsadam/compose-dev`  
`cd compose-dev`  
`make run`   

To perform integration tests, once the `make run` command has been successfully run, in another terminal, type the following:  
`pytest`   

