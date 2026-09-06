from SIunit import SI_prefix
#replace the current_dict with just current (somehow find the mapping)

class Circuit(): 
    def __init__(self):
        self.components = [] 
        self.component_map = {} 
        self.node_map = {} # node_name -> matrix index 
        self.extra_unknown_map = {} # this is for the extra equations for the current in the votlage sources
        self.reversed_node_map = {} # matrix index -> node_name
        self.voltages = [] # node -> voltage
        self.currents = [] # component -> current
       
        
   
       
    def addComponent(self,comp): 
        self.components.append(comp) 
        name = comp.name
        self.component_map[name] = len(self.components) - 1

        for i in comp.nodes: 
            if i != "0" and i not in self.node_map: 
                if len(self.node_map) == 0: 
                    self.node_map[i] = 0 
                    self.reversed_node_map[0] = i 
                else: 
                    length = len(self.node_map)
                    self.node_map[i] = length
                    self.reversed_node_map[length] = i 

    def __repr__(self): 
        netlist = [] 
        for component in self.components: 
            netlist.append(repr(component)) 
        
        return "\n".join(netlist)   
    
    def parseResultsMatrix(self,results_matrix,mode): 
        self.voltages = [None] * len(self.node_map)
        self.currents = [None] * len(self.component_map)


        # Voltage
        for i in range(len(self.node_map)): 
            value = results_matrix[i][-1]
            self.voltages[i] = value 

        # Currents 
        for i in self.components: 
            i.calcVoltage(self.voltages,self.node_map)
            current = i.calcCurrent(results_matrix,self.node_map,self.extra_unknown_map,mode)
            index = self.component_map[i.name]
            self.currents[index] = current

            i.calcPower() 

        
    def printValues(self): 

        for node in self.node_map: 
            unformatted_value = self.voltages[self.node_map[node]]
            voltage =round( SI_prefix(unformatted_value),3)
            print(f"{f"V({node})":<10} :       {voltage}V")
        
        for component in self.components: 
            current = SI_prefix(component.current)
             
            print(f"{f"I({component.name})":<10} :       {current}A")

        for component in self.components: 
            value = SI_prefix(component.power)
            print(f"{f"P({component.name})":<10} :       {value}W")