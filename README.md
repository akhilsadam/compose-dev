<!-- ⚠️ This README has been generated from the file(s) "blueprint.md" ⚠️--><h1 align="center">compose</h1>
<p align="center">
  <b>An containerized Flask-Redis-Kubernetes application to analyze the role of music in communication. Final Project for COE332.</b></br>
  <sub><sub>
</p>

<br />



[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#implementation)

#  Implementation

This project uses Python3 (in particular Flask), Docker for containerization, and Kubernetes for deployment. Specific Python3 package requirements can be found <a href="https://github.com/akhilsadam/compose-dev/blob/main/requirements.txt">here</a>. R and the npm package `@appnest/readme` by Andreas Mehlsen are used for documentation, but are not part of the API and will not be documented.

The source is available <a href="https://github.com/akhilsadam/compose-dev">here</a>.

A list of important files can be found below.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#files)

##  Files

 - `app/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The application folder.
 - `test/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains testfiles.
 
 - `Makefile`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A makefile for ease of compilation.
 - `docker/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A folder containing dockerfiles for containerization.
 - `deployment/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A folder containing yaml files for Kubernetes test and production deployments.
 - `flask-data/` and `redis-data/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Volume mount folders for Docker-only testing.
 - `scripts`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains run scripts for Docker-only testing.
 - `requirements.txt` and `require-worker.txt`:&nbsp;&nbsp;&nbsp;&nbsp;The list of Python3 requirements for the API and worker containers.

 - `doc/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A documentation folder.
 - `blueprint.*` and `package*`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Files for automatic README generation.
 
 - `core.py`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The main Python file for API containers.
 - `worker.py`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The main Python file for worker containers.
### The App/ Directory

- `api/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains API route definitions in Python.
- `shaft/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains additional functions for API container usage.
- `queue/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains job MPI functions for both API and worker containers.
- `static/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains static files for browser use.
- `quarry/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains worker task definitions.
- `core/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains analysis and processing functions for worker use.
- `templates/`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains Jinja2 templates for browser use.

- `assets.py`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Collects static files for browser use.
- `log.py`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Defines Python logger.
- `options.py`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Defines global options, like the application url.
- `redisclient.py`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contains helper Redis methods.
- `routes.py`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Collects the API route definitions.
- `schema.py`:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Defines basic route schemata.





[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#input-data)

##  Input Data

- The application uses midi data from several composers, listed below. In addition, self-generated datasets are also used upon user request.  

```
Kawaki wo Ameku (Crying for Rain) - Minami (arr. Animenz)
Unravel - TK from Ling Tosite Sugire (arr. Animenz)
Iris - Cynax
Bokura mada Underground (We're Still Underground) - E ve
Higurashi no Naku Koro ni - Shimamiya Eiko (Main Theme)
Vogel im Kafig (Bird in a Cage) - Sawano Hiroyuki
One Last Kiss - Utada Hikaru
```
```
Moonlight Sonata (1st Movement) - Ludwig van Beethoven
Opus 10, Number 4 (Torrent) - Fryderyk Franciszek Chopin
```

- DO NOT download / distribute these midi reductions in any form or fashion (they are only available here under fair use).



[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#installation--usage)

#  Installation & Usage

A user can build this project from source, use the provided Docker containers on DockerHub, or deploy to a Kubernetes cluster.  
A Docker installation is required for source builds, as we build and run a Docker image.




The following commands are all terminal commands, and are expected to run on a Ubuntu 20.04 machine with Python3, and are written in that fashion. Mileage may vary for other systems. 

### From Source:

Clone the repository and then use the makefile to start the containers (make sure Docker has been installed prior).  
`git clone https://github.com/akhilsadam/compose-dev`  
`cd compose-dev`  
`make iterate`  

Now either use a browser or a curl utility to interact with the application at `https://localhost:5026/`. Further instructions are provided in the writeup, so please refer there as necessary.

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




[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#api--)

##  API  

<details>
<summary> Complete API Reference </summary>


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#rest-api)

##  REST API:
### ENDPOINT: `/`
 - Description: Get homepage HTML
 - Parameters: 
   -  N/A
 - Responses: 
   -  A `200` response will : Return homepage HTML

 - Example: `curl -X GET http://0.0.0.0:5026/ -H "accept: application/json"`


### ENDPOINT: `/api/doc`
 - Description: Get API HTML
 - Parameters: 
   -  N/A
 - Responses: 
   -  A `200` response will : Return API HTML

 - Example: `curl -X GET http://0.0.0.0:5026/api/doc -H "accept: application/json"`


### ENDPOINT: `/api/save`
 - Description: Get API as rendered string
 - Parameters: 
   -  N/A
 - Responses: 
   -  A `200` response will : Return rendered API as string

 - Example: `curl -X GET http://0.0.0.0:5026/api/save -H "accept: application/json"`


### ENDPOINT: `/country`
 - Description: Get all possible countries.
 - Parameters: 
   -  N/A
 - Responses: 
   -  A `200` response will : Return a list of countries.

 - Example: `curl -X GET http://0.0.0.0:5026/country -H "accept: application/json"` yields: 
```  
 [  
     "United_States"  
 ]
```

### ENDPOINT: `/country/{country}`
 - Description: Get data for a single country.
 - Parameters: 
   -  `country`	:	Value (name) of country to be queried.	An example would be : `United_States`
 - Responses: 
   -  A `200` response will : Return all matching (queried country) sightings as json.

 - Example: `curl -X GET http://0.0.0.0:5026/country/United_States -H "accept: application/json"` yields: 
```  
 [  
     {  
         "city": "Olathe",  
         "country": "United_States",  
         "duration_minutes": "6",  
         "enters": "10 above SSW",  
         "exits": "10 above ENE",  
         "max_elevation": "28",  
         "region": "Kansas",  
         "sighting_date": "Thu Feb 17/06:13 AM",  
         "spacecraft": "ISS",  
         "utc_date": "Feb 17, 2022",  
         "utc_offset": "-6.0",  
         "utc_time": "12:13"  
     },  
 ....  
     {  
         "city": "Nantucket",  
         "country": "United_States",  
         "duration_minutes": "3",  
         "enters": "19 above NNW",  
         "exits": "10 above NNE",  
         "max_elevation": "19",  
         "region": "Massachusetts",  
         "sighting_date": "Sat Feb 26/04:56 AM",  
         "spacecraft": "ISS",  
         "utc_date": "Feb 26, 2022",  
         "utc_offset": "-5.0",  
         "utc_time": "09:56"  
     }  
 ]
```

### ENDPOINT: `/country/{country}/region`
 - Description: Get data for all regions of a certain country.
 - Parameters: 
   -  `country`	:	Value (name) of country to be queried.	An example would be : `United_States`
 - Responses: 
   -  A `200` response will : Return all matching regions for the queried country as json.

 - Example: `curl -X GET http://0.0.0.0:5026/country/United_States/region -H "accept: application/json"` yields: 
```  
 [  
     "Kansas",  
     "Kentucky",  
     "Louisiana",  
     "Maine",  
     "Mariana_Islands",  
     "Maryland",  
     "Massachusetts"  
 ]
```

### ENDPOINT: `/country/{country}/region/{region}`
 - Description: Get all data for a specific region of a certain country.
 - Parameters: 
   -  `country`	:	Value (name) of country to be queried.	An example would be : `United_States`
   -  `region`	:	Value (name) of region to be queried.	An example would be : `Kansas`
 - Responses: 
   -  A `200` response will : Return all matching results for the queried region as json.

 - Example: `curl -X GET http://0.0.0.0:5026/country/United_States/region/Kansas -H "accept: application/json"` yields: 
```  
 [  
     {  
         "city": "Olathe",  
         "country": "United_States",  
         "duration_minutes": "6",  
         "enters": "10 above SSW",  
         "exits": "10 above ENE",  
         "max_elevation": "28",  
         "region": "Kansas",  
         "sighting_date": "Thu Feb 17/06:13 AM",  
         "spacecraft": "ISS",  
         "utc_date": "Feb 17, 2022",  
         "utc_offset": "-6.0",  
         "utc_time": "12:13"  
     },  
 ....  
     {  
         "city": "Yates_Center",  
         "country": "United_States",  
         "duration_minutes": "1",  
         "enters": "12 above N",  
         "exits": "10 above N",  
         "max_elevation": "12",  
         "region": "Kansas",  
         "sighting_date": "Sat Feb 26/05:29 AM",  
         "spacecraft": "ISS",  
         "utc_date": "Feb 26, 2022",  
         "utc_offset": "-6.0",  
         "utc_time": "11:29"  
     }  
 ]
```

### ENDPOINT: `/country/{country}/region/{region}/city`
 - Description: Get all cities for a specific region of a certain country.
 - Parameters: 
   -  `country`	:	Value (name) of country to be queried.	An example would be : `United_States`
   -  `region`	:	Value (name) of region to be queried.	An example would be : `Kansas`
 - Responses: 
   -  A `200` response will : Return all matching cities for the queried region and country as json.

 - Example: `curl -X GET http://0.0.0.0:5026/country/United_States/region/Kansas/city -H "accept: application/json"` yields: 
```  
 [  
     "Olathe",  
     "Osborne",  
     "Oskaloosa",  
     "Oswego",  
     "Ottawa",  
     "Paola",  
     "Phillipsburg",  
     "Pittsburg",  
     "Pratt",  
     "Russell",  
     "Saint_Francis",  
     "Saint_John",  
     "Salina",  
     "Scott_City",  
 ....  
     "Sublette",  
     "Syracuse",  
     "Tallgrass_Prairie_National_Preserve",  
     "Topeka",  
     "Tribune",  
     "Troy",  
     "Ulysses",  
     "WaKeeny",  
     "Washington",  
     "Wellington",  
     "Westmoreland",  
     "Wichita",  
     "Winfield",  
     "Yates_Center"  
 ]
```

### ENDPOINT: `/country/{country}/region/{region}/city/{city}`
 - Description: Get all information for a specific city of a region of a certain country.
 - Parameters: 
   -  `country`	:	Value (name) of country to be queried.	An example would be : `United_States`
   -  `region`	:	Value (name) of region to be queried.	An example would be : `Kansas`
   -  `city`	:	Value (name) of city to be queried.	An example would be : `Wichita`
 - Responses: 
   -  A `200` response will : Return all information for the queried city as json.

 - Example: `curl -X GET http://0.0.0.0:5026/country/United_States/region/Kansas/city/Wichita -H "accept: application/json"` yields: 
```  
 [  
     {  
         "city": "Wichita",  
         "country": "United_States",  
         "duration_minutes": "6",  
         "enters": "10 above S",  
         "exits": "10 above ENE",  
         "max_elevation": "25",  
         "region": "Kansas",  
         "sighting_date": "Thu Feb 17/06:12 AM",  
         "spacecraft": "ISS",  
         "utc_date": "Feb 17, 2022",  
         "utc_offset": "-6.0",  
         "utc_time": "12:12"  
     },  
 ....  
     {  
         "city": "Wichita",  
         "country": "United_States",  
         "duration_minutes": "1",  
         "enters": "12 above N",  
         "exits": "10 above N",  
         "max_elevation": "12",  
         "region": "Kansas",  
         "sighting_date": "Sat Feb 26/05:29 AM",  
         "spacecraft": "ISS",  
         "utc_date": "Feb 26, 2022",  
         "utc_offset": "-6.0",  
         "utc_time": "11:29"  
     }  
 ]
```

### ENDPOINT: `/data`
 - Description: Updates the list of data dictionaries.
 - Parameters: 
   -  N/A
 - Responses: 
   -  A `201` response will : Updated data dictionary list.

 - Example: `curl -X POST http://0.0.0.0:5026/data -H "accept: application/json"` yields: 
```  
 "Data updated."
```

### ENDPOINT: `/epoch`
 - Description: Get all possible epochs.
 - Parameters: 
   -  N/A
 - Responses: 
   -  A `200` response will : Return a list of epochs.

 - Example: `curl -X GET http://0.0.0.0:5026/epoch -H "accept: application/json"` yields: 
```  
 [  
     "2022-042T12:00:00.000Z",  
     "2022-042T12:04:00.000Z",  
     "2022-042T12:08:00.000Z",  
     "2022-042T12:12:00.000Z",  
     "2022-042T12:16:00.000Z",  
     "2022-042T12:20:00.000Z",  
     "2022-042T12:24:00.000Z",  
     "2022-042T12:28:00.000Z",  
     "2022-042T12:32:00.000Z",  
     "2022-042T12:36:00.000Z",  
     "2022-042T12:40:00.000Z",  
     "2022-042T12:44:00.000Z",  
     "2022-042T12:48:00.000Z",  
     "2022-042T12:52:00.000Z",  
 ....  
     "2022-057T11:08:56.869Z",  
     "2022-057T11:12:56.869Z",  
     "2022-057T11:16:56.869Z",  
     "2022-057T11:20:56.869Z",  
     "2022-057T11:24:56.869Z",  
     "2022-057T11:28:56.869Z",  
     "2022-057T11:32:56.869Z",  
     "2022-057T11:36:56.869Z",  
     "2022-057T11:40:56.869Z",  
     "2022-057T11:44:56.869Z",  
     "2022-057T11:48:56.869Z",  
     "2022-057T11:52:56.869Z",  
     "2022-057T11:56:56.869Z",  
     "2022-057T12:00:00.000Z"  
 ]
```

### ENDPOINT: `/epoch/{name}`
 - Description: Get data for a single epoch.
 - Parameters: 
   -  `name`	:	Value of epoch to be queried.	An example would be : `2022-042T12:04:00.000Z`
 - Responses: 
   -  A `200` response will : Return epoch information for first matching epoch as json.

 - Example: `curl -X GET http://0.0.0.0:5026/epoch/2022-042T12:04:00.000Z -H "accept: application/json"` yields: 
```  
 {  
     "EPOCH": "2022-042T12:04:00.000Z",  
     "X": {  
         "#text": "-4483.2181885642003",  
         "@units": "km"  
     },  
     "X_DOT": {  
         "#text": "2.63479158884966",  
         "@units": "km/s"  
     },  
     "Y": {  
         "#text": "-4839.4374260438099",  
         "@units": "km"  
     },  
     "Y_DOT": {  
         "#text": "-4.3774148889971602",  
         "@units": "km/s"  
     },  
     "Z": {  
         "#text": "-1653.1850590663901",  
         "@units": "km"  
     },  
     "Z_DOT": {  
         "#text": "5.7014974180323597",  
         "@units": "km/s"  
     }  
 }
```

### ENDPOINT: `/pdf`
 - Description: Get writeup HTML
 - Parameters: 
   -  N/A
 - Responses: 
   -  A `200` response will : Return writeup HTML

 - Example: `curl -X GET http://0.0.0.0:5026/pdf -H "accept: application/json"`


</details>

<!-- 
[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#table-of-contents)

##  Table of Contents

* [ Implementation](#-implementation)
	* [ Files](#-files)
		* [The App/ Directory](#the-app-directory)
	* [ Input Data](#-input-data)
* [ Installation & Usage](#-installation--usage)
		* [From Source:](#from-source)
		* [Kubernetes Deployment:  ](#kubernetes-deployment--)
		* [From Docker](#from-docker)
	* [ API  ](#-api--)
	* [ REST API:](#-rest-api)
		* [ENDPOINT: `/`](#endpoint-)
		* [ENDPOINT: `/api/doc`](#endpoint-apidoc)
		* [ENDPOINT: `/api/save`](#endpoint-apisave)
		* [ENDPOINT: `/country`](#endpoint-country)
		* [ENDPOINT: `/country/{country}`](#endpoint-countrycountry)
		* [ENDPOINT: `/country/{country}/region`](#endpoint-countrycountryregion)
		* [ENDPOINT: `/country/{country}/region/{region}`](#endpoint-countrycountryregionregion)
		* [ENDPOINT: `/country/{country}/region/{region}/city`](#endpoint-countrycountryregionregioncity)
		* [ENDPOINT: `/country/{country}/region/{region}/city/{city}`](#endpoint-countrycountryregionregioncitycity)
		* [ENDPOINT: `/data`](#endpoint-data)
		* [ENDPOINT: `/epoch`](#endpoint-epoch)
		* [ENDPOINT: `/epoch/{name}`](#endpoint-epochname)
		* [ENDPOINT: `/pdf`](#endpoint-pdf)
	* [ Contributors](#-contributors)
	* [ License](#-license) -->

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#contributors)

##  Contributors
	

| [Anneris Rodriguez](undefined) | [Akhil Sadam](https://github.com/akhilsadam) | [David Ventura Diaz](undefined) |
|:--------------------------------:|:----------------------------------------------:|:---------------------------------:|



[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.png)](#license)

##  License
	
Licensed under [MIT](https://opensource.org/licenses/MIT).