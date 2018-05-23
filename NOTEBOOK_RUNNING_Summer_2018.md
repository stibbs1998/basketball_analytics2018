# Week 1 (5/21/2018 - 5/25/2018)

[Second Spectrum](https://www.secondspectrum.com/)

To-do
* Read in data efficiently. 
* [Running average](https://en.wikipedia.org/wiki/Moving_average) for position (5 point smoothing?)
* Calc velocities and *accelerations*. Both should be smoother now. 

How is data stored in a [JSON file](http://www.json.org/)??
Data in a JSON file is structured very similarly to that of a python dictionary.  Here's an example:

{ <br/>
> "value_string": "hello world!",<br/>
> "value_number": 3.14159265,<br/>
> "value_array":[<br/>
  >>  a, <br/>
   >> b, <br/>
    >> c, <br/>
    >> ], <br/>
> "value_object":{ <br/>
    >> "A":1 <br/>
    >>"B":2 <br/>
    >> }, <br/>
> "Kevin Durant is a snake": true <br/>
} <br/>

The name of each value is defined in quotes, followed by a colon and the assigned value.  Commas are used to seperate values. As seen above, values can be defined as:
* strings
* numbers
* objects
* arrays
* booleans
Booleans are written as *true, false*, and *null*, opposed to *True, False*, and *None* in Python.  Using the [json module](https://docs.python.org/2/library/json.html), when a JSON file is read into Python, the file is read in as a dictionary, and the name of each value is accessible as a unicode key within the dictionary.  Arrays are converted into lists, and *true,false*, and *null* are converted into *True, False*, and *None*. 
