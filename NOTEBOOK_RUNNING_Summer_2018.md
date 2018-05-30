# Week 1 (5/21/2018 - 5/25/2018)

[Second Spectrum](https://www.secondspectrum.com/)

To-do
* Read in data efficiently. 
* [Running average](https://en.wikipedia.org/wiki/Moving_average) for position (5 point smoothing?)
* Calc velocities and *accelerations*. Both should be smoother now. 

How is data stored in a [JSON file](http://www.json.org/)??
Data in a JSON file is structured very similarly to that of a python dictionary.  Here's an example:
```
{ 
 "value_string": "hello world!",
 "value_number": 3.14159265,
 "value_array":[
   a, 
   b, 
   c, 
   ],
 "value_object":{ 
   "A":1 
   "B":2 
   }, 
 "Kevin Durant is a snake": true
 }
```
The name of each value is defined in quotes, followed by a colon and the assigned value.  Commas are used to seperate values. As seen above, values can be defined as:
* strings
* numbers
* objects
* arrays
* booleans 


Booleans are written as *true, false*, and *null*, opposed to *True, False*, and *None* in Python.  Using the [json module](https://docs.python.org/2/library/json.html), when a JSON file is read into Python, the file is read in as a dictionary, and the name of each value is accessible as a unicode key within the dictionary.  Arrays are converted into lists, and *true,false*, and *null* are converted into *True, False*, and *None*. 

The tracking data files we have are known as [JSONL files](http://jsonlines.org/).  The only difference between JSONL files and JSON files is that instead of a comma being used to seperate values, a new line is used to indicate a new value.  Compared to the XML data files, the JSONL files have all of the same data: the positions of each player on the court and the ball in the 3-D plane every 0.04 seconds, along with corresponding player IDs, the players seperated by team, and the game clock.  The only real differences is that an entire game is stored in one JSONL file whereas the XML files are seperated into each quarter.  Therefore in the JSONL files there is a value at each momement to signify what quarter it is.



# Week 2 (5/29/2018 - 6/1/2018)

To-do
* Get player velocities, accelerations, work, etc. set
* Try to seperate data points into offense and defense
   * different speeds on offense v. defense?
   * more work exerted on which side?
* Compare average speeds of players on offense and defense and see if any difference is noticeable
