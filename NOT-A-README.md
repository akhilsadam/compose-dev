# The actual readme for the compose-dev repository (the README.md applies to the project itself).


# Files (and what they should do)
## api
- `app/api/` contains all the routes to do everything, separated by different classes. See `app/api/example.py` for an example.
 - `app/api/register` will generate api and run some basic tests on every route (tests that they do return an output).
 - `app/api/schema` lists possible output types (you can use these names in the route docstrings).
- `app/core/` contains all the main chord-analysis code, with example data.
- `app/log.py` defines the default logger.
- `app/options.py` defines default options, like the Flask and Redis urls, among others.
## data
 - `data` contains Redis backups for persistency.

## other
 - `app/static`, `app/templates` can be ignored for now. Those are GUI related stuff that would be fairly simple and of last importance.

# Files (and what needs to be done to them!)

```
TBW (to be written)
```

Note we use a git submodule to copy over files from the `compose-wa` repository into the app/core folder (there should be no additional work necessary on your end when you do a `git pull`).

# LIST OF TASKS:

## Current REST API / CRUD (with current assignees):

<details>
<summary>Details (dropdown)</summary>

### [@Akhil]:
#### A Redis database will be used to store the following data: (example objects can be found in `\app\core\midi`, `\app\core\chord-progressions`, `\app\core\sf2\`)
##### Immutable data packaged with the application (will be in `db=0`):
- Array: a table of chords, each with their corresponding emotion vector.
- Array: a (matrix) table of chord-modulations, each with their resulting emotion vector.
- Floats: a set of parameters describing the relation between the resultant emotional value and the individual chord / chord-modulations. (Any necessary parameters for the theoretical model will be stored here.)
##### Fields  (can have multiple items) (will be in `db=1`):
- Song Object
 - MusicPy: A song object stored in the default musicpy object via pickling.
  - Examples provided, CRUD amenable.
 - Chord Progression: A chord progression stored as a list of dictionaries, with chord names and lengths.
  - Examples provided, CRUD amenable.
- Emotion Object : An emotion object storing the overall emotion vector, as well as the emotion vector time-series (matrix).
- Examples provided (will be automatically generated), CRUD amenable.
- SF2: A couple of instrument files will be provided for playing songs. 
 - Examples provided, immutable.

### [@Anneris & @David]:
#### Generic CRUD operations will be performed on the database as follows:
##### Create a song / chord-progression field in the database
- via an uploaded MIDI file or a chord-progression JSON input
##### Read out song / chord-progression parameters as JSON, which include:
- BPM (a list of dictionaries so as to include time-changes)
- Total number of chords
- Chord types (a list of strings)
- Total number of notes
- Notes (a list of strings)
- Note Intervals (a list of floats)
- An overall emotion vector calculated theoretically
- An overall emotion vector calculated by comparison to known songs
- An instantaneous emotion vector time series (a matrix) calculated theoretically
- An instantaneous emotion vector time series (a matrix) calculated by comparison to known songs 
##### Update all song / chord-progression parameters described above.
##### Delete a song / chord-progression field from the database.

### [@Akhil]:
#### Analysis / Other Routes (output will be in `db=2`):
- A plot of the instantaneous emotion vector time series (a matrix) calculated theoretically
- A plot of the instantaneous emotion vector time series (a matrix) calculated by comparison to known songs
- A plot of related songs on emotion-based axes using a theoretical transformation.
- A plot of related songs on emotion-based axes by comparison to other songs by similarity methods (also using theoretical emotion vectors to calculate similarity).
- A float value denoting similarity between two songs in the database

</details>

## Kubernetes Workers & Redis Job Queue: TBD

<details>
<summary>Details (dropdown)</summary>

TBD
 - at least 2 back-end workers, a Redis worker, and a Flask worker
 - the queue will be on database `db=3`

</details>

## WriteUp : TBD

<details>
<summary>Details (dropdown)</summary>

TBD 
- will use the doc folder markdown & makefile commands to generate README and PDF.
- plan on using Kroki and Mermaid for the software diagram. 
- some theory notes on implementation will need to be added in by @Akhil.

</details>

## Video Demo : TBD

<details>
<summary>Details (dropdown)</summary>

TBD (Assuming @David would like to do this, so will leave it to him when we finish the other sections)

</details>