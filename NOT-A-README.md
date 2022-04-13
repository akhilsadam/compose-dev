# The actual readme for the compose-dev repository (the README.md applies to the project itself).


Files (and what they should do)
```
```
Files (and what needs to be done to them!)
```
```

1) We use a git submodule to copy over files from the `compose-wa` repository (there should be no work necessary on your end).

We need to add the Kubernetes workers into this framework (I think that can wait till next week, since that may make it harder to test...)

# Current API (with current assignees):

[Akhil]:
## A Redis database will be used to store the following data: (example objects can be found in `\app\core\midi`, `\app\core\chord-progressions`, `\app\core\sf2\`)
### Immutable data packaged with the application:
- Array: a table of chords, each with their corresponding emotion vector.
- Array: a (matrix) table of chord-modulations, each with their resulting emotion vector.
- Floats: a set of parameters describing the relation between the resultant emotional value and the individual chord / chord-modulations. (Any necessary parameters for the theoretical model will be stored here.)
### Fields  (can have multiple items):
- Song Object - MusicPy: A song object stored in the default musicpy object via pickling.
- Examples provided, CRUD amenable.
- Chord Progression: A chord progression stored as a list of dictionaries, with chord names and lengths.
- Examples provided, CRUD amenable.
- Emotion Object : An emotion object storing the overall emotion vector, as well as the emotion vector time-series (matrix).
- Examples provided (will be automatically generated), CRUD amenable.
- SF2: A couple of instrument files will be provided for playing songs. 
Examples provided, immutable.

[Anneris & David]:
## Generic CRUD operations will be performed on the database as follows:
### Create a song / chord-progression field in the database
- via an uploaded MIDI file or a chord-progression JSON input
### Read out song / chord-progression parameters as JSON, which include:
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
### Update all song / chord-progression parameters described above.
### Delete a song / chord-progression field from the database.

[Akhil]:
## Analysis / Other Routes:
- A plot of the instantaneous emotion vector time series (a matrix) calculated theoretically
- A plot of the instantaneous emotion vector time series (a matrix) calculated by comparison to known songs
- A plot of related songs on emotion-based axes using a theoretical transformation.
- A plot of related songs on emotion-based axes by comparison to other songs by similarity methods (also using theoretical emotion vectors to calculate similarity).
- A float value denoting similarity between two songs in the database
