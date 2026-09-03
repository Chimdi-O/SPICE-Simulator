from Circuit.Circuit import Circuit
from Circuit.Components import Resistor, Inductor, Capacitor, VoltageSource, CurrentSource
from Simulation.SimulationManager import SimulationManager
import sys 
from Simulation.SimulationTypes.OperatingPoint import OperatingPoint 
from Simulation.SimulationTypes.Transient import Transient 
from SIunit import parseUnits

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

    def parseLine(self,line): 
        line = line.strip()
        
        
        if not line or line.startswith("*"): 
            return 

        elif line.startswith("."): 
            tokens = line[1:].split() 
            directive = self.parseDirectives(tokens)
            self.directive = directive

        else: 
            tokens = line.split() 
            comp = self.parseComponent(tokens)
            self.circuit.addComponent(comp)


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

            

    def parseComponent(self,tokens): 
        
        name = tokens[0].upper() 
        # some type of if statement when we have components with different number of nodes 
        nodes = tokens[1:3]
        str_value = tokens[3]
        num_value = parseUnits(str_value)

        if name  in self.component_names: 
            print(f"Error: Duplicate component name {name} on line {self.current_line}")
            sys.exit() 

        self.component_names.append(name)

        if name.startswith("R"): 
            return Resistor(name,nodes,str_value,num_value)

        elif name.startswith("C"): 
            return Capacitor(name,nodes,str_value,num_value)

        elif name.startswith("L"): 
            return Inductor(name,nodes,str_value,num_value)
        
        elif name.startswith("V"): 
            return VoltageSource(name,nodes,str_value,num_value)
        
        elif name.startswith("I"): 
            return CurrentSource(name,nodes,str_value,num_value)
        
        else: 
            print(f"Error: Unknown component type {name} on line {self.current_line}")
            sys.exit() 

 