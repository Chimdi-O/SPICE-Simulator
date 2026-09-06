from Circuit.Circuit import Circuit
from Circuit.Components import Resistor, Inductor, Capacitor, VoltageSource, CurrentSource
from Simulation.SimulationManager import SimulationManager
import sys 
from Simulation.SimulationTypes.OperatingPoint import OperatingPoint 
from Simulation.SimulationTypes.Transient import Transient 
from SIunit import parseUnits
from Simulation.Waveforms import Sinewave 

class Interpreter(): 

    def __init__(self): 
        self.circuit = Circuit()
        self.simulation_manager = SimulationManager(self.circuit) 
        self.component_names = [] 
        self.current_line = 1
        
    def parseFile(self,filepath): 
        self.current_line = 1
        with open(filepath) as f: 
            next(f) #spice skips the first line of the file as its the title 
            self.current_line += 1

            for line in f: 
                self.parseLine(line)
                self.current_line += 1

    def tokenize(self,line): 
        tokens = []
        i = 0 
        extra_characters = ["*",".","(",")"]
        
        while i < len(line): 

            if line[i] in extra_characters: 
                tokens.append(line[i])
                i += 1 

            elif line[i].isalnum(): 
                start = i 
    
                while line[i].isalnum(): 
                    i += 1

                tokens.append(line[start:i])

            elif line[i] == " ": 
                i += 1 

            elif line[i] == "\n": 
                break

            else: 
                print(f"unknown charcter {line[i]} on line {self.current_line}") 
                sys.exit() 

        return tokens 

    def parseLine(self,line): 

        tokens = self.tokenize(line)
     

        if not tokens or tokens[0] == "*": 
            return 
        
        elif tokens[0] == ".": 
            directive = self.parseDirectives(tokens[1:])
            #self.directive = directive

        
        else: 
            component = self.parseComponent(tokens)
            print(component)
            self.circuit.addComponent(component)


    def parseDirectives(self,tokens): 
        directive = tokens[0].lower()
        arguments = tokens[1:]

        if directive == "op": 
            mode  = OperatingPoint(self.circuit)
            self.simulation_manager.directives.append(mode)
            return

        elif directive == "tran": 
            time_step = parseUnits(arguments[0])
            stop_time = parseUnits(arguments[1])
            mode  = Transient(self.circuit,time_step,stop_time)
            self.simulation_manager.directives.append(mode)
            return

        else: 
            print(f"Error: Unknown directive {directive} on line {self.current_line}")
            sys.exit() 

    def parseWaveform(self,tokens): 
        name = tokens.pop(0)

        if tokens.pop(0) != "(": 
            print(f"Error: Expected a opening bracket '(' on {self.current_line}")
            sys.exit() 

        if tokens.pop() != ")": 
            print(f"Error: Expected a closing bracket ')' on {self.current_line}")
            sys.exit() 

        

        if name == "sine": 
            parsed_tokens = [] 
            for i in tokens: 
                parsed_tokens.append(parseUnits(i))
            Waveform = Sinewave(parsed_tokens[0],parsed_tokens[1],parsed_tokens[2])

        else: 
            print(f"Error: Unrecognised waveform '{name}' on line {self.current_line}")
            sys.exit() 
        
        return  Waveform


    def parseComponent(self,tokens): 
        print(tokens)
        
        name = tokens[0].upper() 
        # some type of if statement when we have components with different number of nodes 
        nodes = tokens[1:3]
        tokens = tokens[3:]
        waveform = 0 

        if tokens[0] == "sine": 
            value = 0
            waveform = self.parseWaveform(tokens)
        
 
        elif len(tokens) == 1: 
            value = parseUnits(tokens[0])

        else: 
            print(f"Error: Invalid component parameters on line {self.current_line}")

        if name  in self.component_names: 
            print(f"Error: Duplicate component name {name} on line {self.current_line}")
            sys.exit() 

        self.component_names.append(name)

        if name.startswith("R"): 
            return Resistor(name,nodes,value)

        elif name.startswith("C"): 
            return Capacitor(name,nodes,value)

        elif name.startswith("L"): 
            return Inductor(name,nodes,value)
        
        elif name.startswith("V"): 
            return VoltageSource(name,nodes,value,waveform)
        
        elif name.startswith("I"): 
            return CurrentSource(name,nodes,value,waveform)
        
        else: 
            print(f"Error: Unknown component type {name} on line {self.current_line}")
            sys.exit() 

 