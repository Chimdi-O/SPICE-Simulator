#Development Log 

This is a record of the progress, issues and decisions made during the development of this project 


## 1st Sep 2026 

### Current state 
The program currently has Resistors, Inductors, Capacitors, Voltage Sources and Current Sources implemented and operating point analysis however I believe for certain strange circuit configurations the simulator does not work and I planned to solved that using super nodes.  

## 2nd Sep 2026

### Current state 
part way through implmenting transient analysis to the program. Currently the transient models for capacitors and inductors have been and I am halfway through creating the transient class 

### todo
Coding the run() class for the transient class                             

## 3rd Sep 2026 

### Current state 
Transient mode now works for capacitors and inductors 

### todo
Fix the op -> transient error

## 3rd Sep 2026 (later in the day)

### Current state 

The op -> transient error has been fixed (it was just a typo in the netlist). 
There was a problem with the ringing of a RLC circuit where the plot was far too flat and almost like a square wave which turned out to be because I was rounding the voltage values in parseresultsMatrix() function instead of the printvalues() function in the circuit class. 
Now all the features implemented fully function

### todo 

add AC current and voltage sources (should be easy)