# Research & Preliminary Results 

A brief summary of relavant theory and the preliminary results we derive are noted here. Note that the code for sections not depicted above is still experimental and thus should not be considered validated.  

## Elementwise State Representation  

We start by using a vertical model for music - a track is sectioned into individual chords, which are treated separately. This is in line with the ISS rationale - that the individual character of a sound defines its emotion.  

Now using Western musical theory's commonly accepted emotions for particular chords, we create a database mapping a chord to an 'emotional vector'. This is done by parsing a text description for a chord with a natural language processing algorithm called [nrclex](https://pypi.org/project/NRCLex/).

These emotional vectors can then be collated into a matrix and plotted as seen below: 


![](images/image7.png)


Doing a PCA (Principal Component Analysis) transformation on the database to see which emotions are best represented by musical chords, and then plotting these emotional vectors on those axis, we get the following, which presumably explains most of the relations in the selected songs.  

![](images/image5.png)  


## Derivative State Representation  


But this is not what music theory teaches. Most songs are relatively emotionally invariant upon transposition, where the whole song is shifted by a constant pitch. So we should investigate a representation based upon the change between two or more chords.

In [*The Geometry of Musical Chords*](https://dmitri.mycpanel.princeton.edu/files/publications/science.pdf), by Dimitri Tymoczko, we can see that the mapping of all intervals (the distance between any two *notes*, which are discretized pitches along a twelve-tone scale) can be mapped onto a Mobius strip, as seen in the below figure.  

![](images/mp.png)  

Note the top-down symmetry, and that the left boundary is identical to the inverted right boundary. So this figure can be either twisted into a Mobius strip, or converted to a toroidal surface mapping (as in the case of the [Tonnetz](https://en.wikipedia.org/wiki/Tonnetz)). Note further that the upper and lower boundaries are singular, so any motion between chords must reflect across that boundary.  

So we now have a mapping between note pitches and a vector position, so vector displacements can be derived, albeit on a non-Euclidean space. Defining the singularities with judicious use of the modulus operator, a model mapping is derived.  

Using this mapping, we can construct a system of chord changes; a vector derivative denoting emotional change, if you will. We will call this dST, where ST are xy-style coordinates on the above plot, and d is used to denote that this is a time derivative. The full model will not be described here, but the following plot will illustrate the expected model result for two particular pieces.  


![](images/st0.png)  


![](images/st1.png)  


![](images/st2.png)  

So it does seem to capture the repeating nature of these pieces, even if we lose the timescale. Assuming that chords are chosen both for timbre and musical function, and that those generally work in concert, we can use the following linear model to convert dST to the emotional value matrix $\lambda$ by a simple matrix transformation.  

$$\lambda * A = {\partial{ST}}{\partial{t}}$$  

Then this can be applied backward to generate chord progressions that produce/reduce/shap a particular emotion over time.  

For now, we make a sanity test: set $\lambda$ to the unit vector and check that the resulting progression does not sound particularly emotional.  

Doing this for Beethoven's Moonlight Sonata and Unravel, we see the following:  

![Beethoven](images/g0.png)  

![Unravel](images/g1.png)  

So the flatline clearly shows that there is some merit to this investigation. We see that the derivative representation does a very good job of representing the variance (at least in these two examples).

## Conclusion  

So returning to the ISS example, the proper identification of voice changes seems more important than the overall timbre, which is what had primarily been studied.
We hope that more study in this area can lead to appropriate usage of this metacommunication, rather than simply relying on the recipient's deduction skills.

Thank you for reading!