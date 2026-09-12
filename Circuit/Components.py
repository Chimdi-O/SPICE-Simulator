from SIunit import SI_prefix
import math

# Branch voltage is defined as V(node0) - V(node1).
# Positive branch current is defined from node0 -> node1.


class Component(): 
    def __init__(self,name,nodes,value): 
        self.name = name 
        self.nodes = nodes 
        self.value = value
        self.current = 0
        self.voltage = 0 
        self.power = 0 
        self.ac = 0 
    
    def __repr__(self): 
        node_string = " ".join(self.nodes)
        return f"{self.name} {node_string} {SI_prefix(self.value)}"
    
    def stamp_cell_a(self,row,column,value,matrix_a): 
        if row != None and column != None: 
             matrix_a[row][column] += value 
 
    def stamp_cell_b(self,row,value,matrix_b): 
        if row != None:
            matrix_b[row] += value


    def calcPower(self): 
        self.power = self.voltage*self.current
    
    def calcVoltage(self,voltage_dict,node_map):
            node1_V = 0 
            node2_V = 0 
            
            if self.nodes[0] != "0": 
                index = node_map[self.nodes[0]]
                node1_V = voltage_dict[index] 
            
            if self.nodes[1] != "0": 
                index = node_map[self.nodes[1]]
                node2_V = voltage_dict[index] 

            self.voltage = node1_V - node2_V
        
        

class Resistor(Component): 

    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode): 
        g = 1/self.value

        a = node_map.get(self.nodes[0])
        b = node_map.get(self.nodes[1])

        self.stamp_cell_a(a,a,g,matrix_a)
        self.stamp_cell_a(a,b,-g,matrix_a)
        self.stamp_cell_a(b,a,-g,matrix_a)
        self.stamp_cell_a(b,b,g,matrix_a)

    
    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode): 
            self.current = self.voltage/self.value
            return self.current
        
  
class Capacitor(Component): 

    def __init__(self,name,nodes,value):
        super().__init__(name,nodes,value)

        self.R_eq = Resistor(None,self.nodes,None)
        self.I_eq = CurrentSource(None,self.nodes,0)
        self.ac = 1

    def update(self,time_step,time): 
         self.R_eq.value = time_step/self.value
         self.I_eq.value = -(self.value * self.voltage)/time_step 

    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode): 
        if mode == "op": 
            pass 
          
        elif mode == "tran":
            self.R_eq.stamp(matrix_a,matrix_b,node_map,extra_unknown_map,mode)  
            self.I_eq.stamp(matrix_a,matrix_b,node_map,extra_unknown_map,mode)             
    
    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode):
        if mode == "op": 
            self.current = 0 
        
        elif mode == "tran": 
            self.current = self.voltage/self.R_eq.value + self.I_eq.value

        return self.current
    
        
class Inductor(Component): 
    #at the start of a new time step self.current represents the old current 
    def __init__(self,name,nodes,value):
        super().__init__(name,nodes,value)
        self.R_eq = Resistor(None,self.nodes,None)
        self.I_eq = CurrentSource(None,self.nodes,0)
        self.ac = 1

    def update(self,time_step,time): 
            self.R_eq.value = self.value/time_step
            self.I_eq.value =  self.current
   

    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode):
        if mode == "op": # in OP inductor is a short which means a voltage source with an inductance of zero1``
            a = node_map.get(self.nodes[0])
            b = node_map.get(self.nodes[1])
            c = extra_unknown_map.get(self.name)

            self.stamp_cell_a(a,c,1,matrix_a)
            self.stamp_cell_a(b,c,-1,matrix_a)
            self.stamp_cell_a(c,a,1,matrix_a)
            self.stamp_cell_a(c,b,-1,matrix_a)
            matrix_b[c] = 0

        if mode == "tran": 
            self.R_eq.stamp(matrix_a,matrix_b,node_map,extra_unknown_map,mode)  
            self.I_eq.stamp(matrix_a,matrix_b,node_map,extra_unknown_map,mode) 
            

    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode): 
        if mode == "op": 
            index = extra_unknown_map[self.name]
            self.current = results_matrix[index][-1]

        elif mode == "tran": 
            self.current = self.voltage/self.R_eq.value + self.I_eq.value

        return self.current

       

class VoltageSource(Component): 
    def __init__(self,name,nodes,value,waveform=0):
        super().__init__(name,nodes,value)
        self.waveform = waveform 
        if self.waveform: 
            self.ac = 1 
            self.dc_offset = value 

    def __repr__(self):
        if self.ac == 1: 
            node_string = " ".join(self.nodes)
            return f"{self.name} {node_string} {self.waveform.name}({SI_prefix(self.value)} {SI_prefix(self.waveform.amplitude)} {SI_prefix(self.waveform.frequency)})"

        else:
            return super().__repr__()

    def update(self,time_step,time): 
        self.value = self.waveform.value(time) + self.dc_offset
        
      

    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode):

        a = node_map.get(self.nodes[0])
        b = node_map.get(self.nodes[1])
        c = extra_unknown_map.get(self.name)

        self.stamp_cell_a(a,c,1,matrix_a)
        self.stamp_cell_a(b,c,-1,matrix_a)
        self.stamp_cell_a(c,a,1,matrix_a)
        self.stamp_cell_a(c,b,-1,matrix_a)
        matrix_b[c] = self.value


    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode): 
        index = extra_unknown_map[self.name]
        self.current = results_matrix[index][-1]
        return self.current


class CurrentSource(Component):
    def __init__(self,name,nodes,value,waveform=0):
        super().__init__(name,nodes,value)
        self.waveform = waveform 
        if self.waveform: 
            self.ac = 1 
    def __repr__(self):
        if self.ac == 1: 
            node_string = " ".join(self.nodes)
            return f"{self.name} {node_string} {self.waveform.name}({SI_prefix(self.value)} {SI_prefix(self.waveform.amplitude)} {SI_prefix(self.waveform.frequency)})"
        else: 
            return super().__repr__() 

    def update(self,time_step,time): 
        self.value = self.waveform.value(time) + self.value
       
    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode):

        a = node_map.get(self.nodes[0])
        b = node_map.get(self.nodes[1])

        self.stamp_cell_b(a,-self.value,matrix_b)
        self.stamp_cell_b(b,self.value,matrix_b)

    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode):
        self.current = self.value
        return self.current

class Diode(Component): 
    def __init__(self, name, nodes, value=None, Is=1e-14, n=1, T=300):
        super().__init__(name, nodes, value)
        self.Is = Is # saturation current 
        self.n = n  # ideality factor
        self.t = T # tempurature
        self.R_eq = Resistor(None,self.nodes,None)
        self.I_eq = CurrentSource(None,self.nodes,0)
        self.k = 1.380649e-23 #Boltzmann constant J/K
        self.q = 1.602176634e-19 #Electron charge C 
        self.voltage = 0.6
        self.calcCurrent()

    def __repr__(self):
        node_string = " ".join(self.nodes)
        return f"{self.name} {node_string}"

    def update(self):
        Vt = self.k*self.t/self.q

        if self.current == 0: 
            self.R_eq.value = 1e15 
        else: 
            self.R_eq.value = self.n*Vt/self.current

        self.I_eq.value = self.current - self.voltage/self.R_eq.value


    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode):
        self.R_eq.stamp(matrix_a,matrix_b,node_map,extra_unknown_map,mode)  
        self.I_eq.stamp(matrix_a,matrix_b,node_map,extra_unknown_map,mode) 

    def calcCurrent(self,results_matrix=None,node_map=None,extra_unknown_map=None,mode=None): 
            Vt = self.k * self.t / self.q
            exp_arg = self.voltage / (self.n * Vt)
            #exp_arg = min(exp_arg, 500)

            self.current = self.Is * (math.exp(exp_arg) - 1)
            return self.current


