<!-- ⚠️ This README has been generated from the file(s) "blueprint.md" ⚠️--><h1 align="center">flask-redis</h1>
<p align="center">
  <b>An containerized Flask webserver to read and update a Redis container. HW05 for COE332.</b></br>
  <sub><sub>
</p>

<br />



[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#implementation)

#  Implementation

This project uses Python3 (in particular Flask), and Docker for containerization. Specific Python3 package requirements can be found <a href="https://github.com/akhilsadam/positional-iss/blob/master/requirements.txt">here</a>.The npm package `@appnest/readme` by Andreas Mehlsen is used for documentation, but is not part of the API and will not be documented.



A list of important files can be found below.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#files)

##  Files

 - `app/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The application folder.
 - `Dockerfile`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A dockerfile for containerization.
 - `Makefile`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A makefile for ease of compilation.
 - `requirements.txt`:&nbsp;&nbsp;&nbsp;&nbsp;The list of Python3 requirements.
 - `core.py`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The main Python file.

### The App/ Directory

- `api/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains API route definitions in Python.






[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#input-data)

##  Input Data

- The application queries data from the following location: <a href="https://raw.githubusercontent.com/wjallen/coe332-sample-data/main/ML_Data_Sample.json">https://raw.githubusercontent.com/wjallen/coe332-sample-data/main/ML_Data_Sample.json</a>, which looks as follows:

```
{
  "meteorite_landings": [
    {
      "name": "Gerald",
      "id": "10001",
      "recclass": "H4",
      "mass (g)": "5754",
      "reclat": "-75.6691",
      "reclong": "60.6936",
      "GeoLocation": "(-75.6691, 60.6936)"
    },
    {
      "name": "Dominique",
      "id": "10002",
      "recclass": "L6",
      "mass (g)": "1701",
      "reclat": "-9.4378",
      "reclong": "49.5751",
      "GeoLocation": "(-9.4378, 49.5751)"
    },
    {
      "name": "Malinda",
      "id": "10003",
      "recclass": "CI1",
      "mass (g)": "3482",
      "reclat": "35.3692",
      "reclong": "61.4206",
      "GeoLocation": "(35.3692, 61.4206)"
    },
    {
      "name": "Mary",
      "id": "10004",
      "recclass": "L5",
      "mass (g)": "5339",
      "reclat": "71.2364",
      "reclong": "-21.9294",
      "GeoLocation": "(71.2364, -21.9294)"
    },
    ...
  ]
}
```




[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#installation--usage)

#  Installation & Usage

A user can build this project from source, or use the provided Docker container on DockerHub.  
A Docker installation is required for source builds, as we build and run a Docker image.




The following commands are all terminal commands, and are expected to run on a Ubuntu 20.04 machine with Python3, and are written in that fashion. Mileage may vary for other systems. We will describe the Docker installation first.   

### From Docker:

#### Install

To install the Docker container, first install Docker.  

  - `apt-get install docker` (if using an Ubuntu machine, else get Docker from <a href="https://www.docker.com/">docker.com</a>.)  
  
Next install the containers.  

  - `docker pull akhilsadam/flask-redis:0.0.2`  

#### Run  

To run the code, please use the `run.sh` script from this repository, with the following terminal command. The terminal should return a link, which can be viewed via a browser or with the `curl` commands documented in the API reference section. (Note this is necessary due to the redis IP address issues.)  

  - `sh run.sh akhilsadam flask-redis 0.0.2`


Now we will move to the source installation.  

### From Source:  

Since this is a Docker build, the requirements need not be installed on the server, as it will automatically be done on the Docker image.  
All commands, unless otherwise noted, are to be run in a terminal (in the home directory of the cloned repository).  

#### Build  

Again, first install Docker.  

  - `apt-get install docker` (if using an Ubuntu machine, else get Docker from <a href="https://www.docker.com/">docker.com</a>.)  
  
Next, clone the repository and change directory into the repository.  

  - `git clone git@github.com:akhilsadam/coe332.git`  

  - `cd coe332/homework05`  


Now build the image.  

  - `make build`  

#### Run  

To run the code, please run the following. The terminal should return a link, which can be viewed via a browser or with the `curl` commands documented in the API reference section.  

  - `make run`  

If the image is not built, it is more appropriate to run the following, to avoid any errors.

  - `make rapid`  




[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#usage--)

##  Usage  



As mentioned above, a browser or the `curl` utility is necessary to view output. All endpoints as mentioned in the REST API section are valid urls, and navigating to those links will return expected output as included in this document.


<details>
<summary> Complete API Reference </summary>


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#rest-api)

##  REST API:

### ENDPOINT (POST) : `/data`
 - Description: Update Redis database with Meteorite Landings data.
 - Parameters: 
   -  N/A
 - Responses: 
   -  A `201` response will : Update the database and return a success message.

 - Example: `curl -X POST http://0.0.0.0:5026/data -H "accept: application/json"`
 - Example Output:
```
Successful Load!
```

 ### ENDPOINT (GET): `/data`
 - Description: Get Meteorite Landings (ML) data from Redis database.
 - Parameters: 
   -  (optional) Start query parameter to index the ML list.
 - Responses: 
   -  A `200` response will : Return the indexed list as JSON.

 - Example: `curl -X GET http://0.0.0.0:5026/data -H "accept: application/json"`
 - Example Output:
```
[{"GeoLocation":"(74.4431, -65.2342)","id":"10010","mass (g)":"3644","name":"Helga","recclass":"L5","reclat":"74.4431","reclong":"-65.2342"},{"GeoLocation":"(-46.4123, 58.0161)","id":"10099","mass (g)":"7317","name":"John","recclass":"H6","reclat":"-46.4123","reclong":"58.0161"},{"GeoLocation":"(-12.9202, 33.6740)","id":"10171","mass (g)":"7419","name":"Marisol","recclass":"CV3","reclat":"-12.9202","reclong":"33.6740"},{"GeoLocation":"(84.8000, 14.6012)","id":"10222",
......
]
```

</details>

<!-- 
[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#table-of-contents)

##  Table of Contents

* [ Implementation](#-implementation)
	* [ Files](#-files)
		* [The App/ Directory](#the-app-directory)
	* [ Input Data](#-input-data)
* [ Installation & Usage](#-installation--usage)
		* [From Docker:](#from-docker)
			* [Install](#install)
			* [Run  ](#run--)
		* [From Source:  ](#from-source--)
			* [Build  ](#build--)
			* [Run  ](#run---1)
	* [ Usage  ](#-usage--)
	* [ REST API:](#-rest-api)
		* [ENDPOINT (POST) : `/data`](#endpoint-post--data)
	* [ Contributors](#-contributors)
	* [ License](#-license) -->

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#contributors)

##  Contributors
	

| [Akhil Sadam](https://github.com/akhilsadam) |
|:----------------------------------------------:|



[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#license)

##  License
	
Licensed under [MIT](https://opensource.org/licenses/MIT).