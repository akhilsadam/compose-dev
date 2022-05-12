# Implementation & Functionality

This application makes use of a graphical interface in conjunction with programming interface routes that are typed into the address bar. To navigate to pages that show or return certain data, the user must type the proper route address into the address bar (or click on the link to that route). From there, the page can be interacted with graphically.

Each route contains a set of methods that perform unique functions within the application. In general, most routes will look like this:

[https://isp-proxy.tacc.utexas.edu/as_tacc-2/](https://isp-proxy.tacc.utexas.edu/as_tacc-2/)&lt;routeName>/&lt;variable>

Where the _&lt;routeName>_ section contains one of the route methods written below, and the _&lt;variable> _section, if applicable, contains a variable as needed by the route (usually, this variable is the song ID). It is important to note that a) no angle brackets should be written into the address, and b) only one slash character is necessary between each field.


## Methods

Most routes and methods available in this application interact with the database to allow the user to create, read, update or delete data. This section provides a detailed description of each supported route.

Routes:



* /api/doc
    * A useful page to look at for a first-time user of this application. This page will show an interactable list of all callable routes within the application. When clicked on, each route will open a menu that displays details on the use of that route and a sample output.



![](images/image10.png "image_tooltip")




* /piece 
    * The piece route returns a list of all songs that have been stored within the database in JSON format. Specific details on each song will also be listed, including the song’s ID, name, and music data. 



![](images/image1.png "image_tooltip")




* /piece/&lt;songID>
    * This route returns individual song data. Given a song ID, it will return all data in the database that is stored with that particular song. Similar to the previously listed route.
* /piece/bpm
    * This route returns a list of the bpm (beats per minute) of every song within the database.


![](images/image6.png "image_tooltip")




* /piece/bpm/&lt;songID>
    * Given a song ID, this route will return the bpm of the requested song in JSON format. Similar to the previously listed route.
* /piece/chords
    * This method returns a JSON list of each chord and note used within the database. The chords and notes are separated by song in a list. Therefore, the returned object is a list of lists containing music data.


![](images/image4.png "image_tooltip")




* /piece/chords/&lt;songID>
    * This route returns a JSON list of every chord and note that is stored for the requested song in the database. The list will store all music data in the order that it appears in the song. Similar to the previously listed route.
* /piece/intervals
    * When called, this route returns a JSON list containing the time interval data of each chord or note that is stored for every song in the database. The returned object is a list of lists holding the information for each song in order of song ID.
    

![](images/image13.png "image_tooltip")




* /piece/intervals/&lt;songID>
    * This route returns interval data of the requested song as a JSON list. The note intervals within the list are stored in the order they appear in the song. Similar to the previously listed route.
* /piece/n_chords
    * Returns a JSON list of the number of chords each song in the database contains.


![](images/image3.png "image_tooltip")




* /piece/n_chords/&lt;songID>
    * Returns the number of chords the requested song contains. Similar to the previously listed route.
* /piece/n_notes
    * Returns a JSON list of the number of notes each song in the database contains.


![](images/image9.png "image_tooltip")




* /piece/n_notes/&lt;songID>
    * Returns the number of notes that the requested song contains. Similar to the previously listed route.
* /piece/notes
    * This route returns a JSON list containing a list of the notes for each song in the database.


![](images/image12.png "image_tooltip")




* /piece/notes/&lt;songID>
    * Returns a list of all the notes that the requested song contains. Similar to the previously listed route.
* /play/&lt;songID>
    * Reroutes the user to a page containing a media player that can play the requested song.


![](images/image15.png "image_tooltip")




* /queue
    * The queue route returns a list of all the jobs that have been requested in JSON format. The list includes specific information regarding each individual job, including request ID, completion status, and job type.


![](images/image14.png "image_tooltip")




* /songbank
    * This page allows the user to create, update and delete song data from the database. It contains fields for entering song data and a list of all the songs currently in the database.
        * CREATE: Fill out the song name, bpm, ID, and chord list fields. Make sure the mode is set to ‘CREATE’. Then submit the form.
        * UPDATE: Fill out the song data fields as you wish to update them for a given song. Type the song ID of the song you wish to update. Then submit the form.
        * DELETE: Type the ID of the song you wish to delete. Submit the form.



![](images/image8.png "image_tooltip")



### Analysis

Certain specialized routes and methods in this application allow for the analysis of the data within the database. Below are the analysis routes supported by this application, including routes that return graphical interpretations of emotional value in a song, or eV.

Routes:



* /analyze/value/&lt;songID> 
    * Methods:
        * ‘GET’: returns an eV plot of the requested song.
        * ‘POST’: updates the eV plot of the requested song.


![](images/image7.png "image_tooltip")


This route opens a page that shows the emotional values generated by the musical structure of the requested song over its course. Below this graph, sharing the same x-axis, is a depiction of the requested song as notes over time. In the top right corner of the page, there is an ‘update’ button that updates the graph with the most recent version of the given song data when clicked. This page also contains a media player that can play the requested song.



* /analyze/PCA/emotion
    * Methods:
        * ‘GET’: returns eV data of all stored songs on a Principal Component Analysis graph.
        * ‘POST’: updates the eV plot.


![](images/image5.png "image_tooltip")


Returns a Principal Component Analysis graph of the calculated emotional values of every song stored in the database. The principal component axes are instead based upon the available chords, and so represent the entire manipulable emotional space. The two most relevant such axes have been selected for plotting, and since each axis is a linear combination of the emotional value parameters, the relationship is also given in the axes labels.



* /analyze/PCA/emotion/&lt;songID>
    * Methods:
        * ‘GET’: returns eV data of the requested song on a PCA graph.
        * ‘POST’: updates the eV plot.

![](images/image16.png "image_tooltip")


Similar to the previous route, this route also returns an emotional value PCA graph. This graph will show the data of a single, user-requested song rather than all of the stored songs within the database.


## CRUD Operations


![](images/image11.png "image_tooltip")


The behavioral diagram above illustrates the CRUD operations performance for the [piece API portion](https://github.com/akhilsadam/compose-dev/blob/main/app/api/piece.py). To initialize the application, the user must curl the init route, which will create the example pieces in the repository. Once song data has been loaded, the user can read the data of a single piece by curling the /piece/&lt;int:songid>/ route. Another route is the /piece/&lt;int:songid>/UPDATE, which will update a piece by replacing its data with the user-uploaded data. Finally, the user is able to delete a song from the song-bank by curling /piece/&lt;int:songid>/DELETE. Note that there are more read routes not shown in the diagram for conciseness, as well as another create route. 



## Documentation System  

Below is a sequence diagram illustrating the process of documentation generation.  


![](https://raw.githubusercontent.com/akhilsadam/coe332/main/homework07/img/register.png)  

First, before the user (left-most object) performs any action, the app.routes module initializes the documentation with the help of the flask-apispec package. The app.routes module, via the flask-apispec package, parses the api information from documentation strings in the route code files (here noted as API data routes), and saves it to a file called app/api/api.json, which can be navigated to and downloaded.  

Now consider the user. When the user uses the curl utility or a browser to navigate to /api/save, a HTTP GET request is sent to the app.api.register module, which requests the pre-generated api.json file (also a HTTP request), and converts that to Python objects. Particularly, the module parses out the example input commands and creates a curl command to test the route.  

Then it calls the appropriate route and collects the example output. (In this diagram all API data routes are clustered together as API data routes for simplicity.) With the example data, the API specification is now complete. The app.api.register module now formats everything into a simple Markdown file, which is then returned to the user as a string.  


## Data Format

The application has a couple of songs preloaded into the system. Data is primarily presented in two distinct forms to accommodate the required functionality:

The first format in which the data was stored was as a [musicpy](https://github.com/Rainbow-Dreamer/musicpy) object. The musicpy object stores the beats per minute (BPM), track number and channel, instrument, tempo changes, notes, and intervals, as shown below:

![](images/image16.png "image_tooltip")


![](images/image17.png "image_tooltip")


The example data above is the information for ‘Crying for Rain’ by Animenz in musicpy object format. The data of the songs stored in such format are located in the Redis database 4. From the example above, we observe that the piece has its title, followed by the BPM. Then, it states the track number and the channel it will be playing on. The data also specifies the instrument played for the data, and the start time of the song. Subsequently, the notes of the song are recorded with the tempo change value and the time it will start at. Finally, the song’s intervals are defined since the song is a time data-series. Note that multiple tracks can be defined for a song, and they will have the same format as the example shown above.

The song’s data is stored as a musicpy object to obtain information for analysis, such as the notes, tempo changes, and chords. This data format is more succinct and precise about the time data-series of the song.

The second format in which the data was stored was a JSON list of dictionaries. Each dictionary in the list stores the bars, BPM, chords, name of the song, and time, as shown below:

![](images/image18.png "image_tooltip")


The example data above is a single dictionary entry in the list. The data of the songs stored in such format are located in the Redis database 3. We observe that the dictionary contains the number of bars the song has, the song’s bpm, and chords. Note that the chords (“chd”) has a value “-”, this means that the chords are in musicpy object format, therefore, they are not displayed in the JSON list of dictionaries for conciseness. It also includes the name of the song and time duration. All of the songs stored in a dictionary in the list will have the same format as the example above.

The song’s data is stored as a JSON list of dictionaries to obtain basic information about the song easily. From each dictionary, the bars, bpm, name, and time data can quickly be accessed without concern for details such as notes and chords.
