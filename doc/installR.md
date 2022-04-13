
Important dependencies: <b>Docker</b> is a containerization application that encapsulates the entire program, operating system, and dependencies, and can run even on bare-metal servers. <b>curl</b> is a command-line interface (CLI) tool that allows users to request data and otherwise interact with an HTTPS application. <b>Make</b> is another CLI tool that uses files called Makefiles to alias several commands to a single word, which is typically run as `make <command>`.  

Simply pulling the Docker container from DockerHub onto the server is sufficient for installation, given a Docker install on the machine. Upon entering the Run command in a terminal, a webpage url will be returned, which can be viewed through either a browser or the `curl` utility. For a source installation, a makefile is also provided with the application, so a Docker image can be constructed and run automatically.  


## Usage   

The HTTPS application uses a REST (Representational State Transfer) API, a particular application programming interface architecture, implemented in HTTPS. In particular for this application, for each endpoint (queryable/navigatable url) listed in the REST API documentation in the appendix, only one of the four HTTP methods (GET/PUT/POST/DELETE) is used upon query, and the user may not choose which: when using `curl`, non-applicable methods will return an error, and browser applications instead automatically select the defined method.  
For this application, GET endpoints will return data, while POST endpoints make internal changes.  
Examples of usage, and a list of all the endpoints, can be seen in the REST API appendix section.  