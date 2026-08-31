

# SPICE Interpreter

This project is a simple SPICE interpreter which is capable of reading a circuit netlist written in SPICE syntax and can provide two analysis types:
- Operating Point
- Transient

## How it works

Input a netlist into the file called **"SpiceTest.txt"** and then run main. The program will then parse the code build the circuit and then run the correct analysis type. 

## Status

The only analysis mode is Operating Point, and the only components are capacitors, inductors, resistors, and voltage sources.

There is no input validation, so bad syntax or an unsolvable circuit will cause errors in the program.  
The ground node should be called **"0"**.

## Why I am building this

I have two motivations behind this project:

1. **Understanding how SPICE actually works**

   SPICE is ubiquitous, so understanding how it functions will allow me to use it more effectively. On top of this, finding out how circuits are solved algorithmically is interesting.

2. **Learning Object‑Oriented Design**

   To build this project with a clear and organised design, concepts must be broken into classes with separate concerns, which provides effective practice at planning and implementing an object‑oriented system.

## Why Python?

Python hides complexities that C++ does not, which allows me to focus on the architecture rather than the syntax.

## Progress

- [x] Parsing SPICE files
- [x] Input validation
- [x] Basic components (resistors, capacitors, inductors, voltage sources)
- [x] Matrix builder / solver
- [x] Operating Point
- [x] Output Formatting
- [x] Current sources
- [x] Power calculations 
- [ ] Transient
- [ ] Waveform plotting
- [ ] AC Voltage sources
- [ ] AC Current source 
- [ ] Supernode analysis
- [ ] Diodes
- [ ] Transistors

