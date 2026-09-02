from Circuit.Circuit import Circuit
from Circuit.Components import Resistor, Inductor, Capacitor, VoltageSource, CurrentSource
from Simulation.SimulationManager import SimulationManager
import sys 
from Simulation.SimulationTypes.OperatingPoint import OperatingPoint 
#from Simulation.SimulationTypes.Transient import Transient 


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
            
            return

        else: 
            print(f"Error: Unknown directive {directive} on line {self.current_line}")
            sys.exit() 

            

    def parseComponent(self,tokens): 
        
        name = tokens[0].upper() 
        # some type of if statement when we have components with different number of nodes 
        nodes = tokens[1:3]
        str_value = tokens[3]
        num_value = self.parseUnits(str_value)

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

    def parseUnits(self,value): 
        i = len(value)-1 # a variable to track the start of the suffix 

        while i >= 0 and value[i].isalpha(): 
            i -= 1

        if  i == -1: 
            print(f"Error: Invalid value {value} on line {self.current_line}")
            sys.exit()
        
        num = value[:i+1]
        unit = value[i+1:]    

        unit_table = {
            "t":1e12, 
            "g":1e9,
            "meg":1e6, 
            "k":1e3, 
            "":1, 
            "m":1e-3, 
            "u":1e-6, 
            "n":1e-9,
            "p":1e-12,
            "f":1e-15}
        
        if unit.lower() not in unit_table: 
            print(f"Error: Invalid unit {unit.lower} on line {self.current_line}")
            sys.exit()

        return float(num) * unit_table[unit.lower()]