from SIunit import SI_prefix

class Component(): 
    def __init__(self,name,nodes,str_value,num_value): 
        self.name = name 
        self.nodes = nodes 
        self.str_value = str_value
        self.num_value = num_value
        self.current = 0
        self.voltage = 0 
        self.power = 0 
    
    def __repr__(self): 
        node_str = " ".join(self.nodes)
        return f"{self.name} {node_str} {self.str_value}"
    
    def stamp_cell_a(self,row,column,value,matrix_a): 
        if row != None and column != None: 
             matrix_a[row][column] += value 
 
    def stamp_cell_b(self,row,value,matrix_b): 
        if row != None:
            matrix_b[row] += value


    def calcPower(self): 
        self.power = self.voltage*self.current
    
    def calcVoltage(self,voltage_dict):
            node1_V = 0 
            node2_V = 0 
            
            if self.nodes[0] != "0": 
                node1_V = voltage_dict[self.nodes[0]] 
            
            if self.nodes[1] != "0": 
                node2_V = voltage_dict[self.nodes[1]] 

            self.voltage = node1_V - node2_V
        
        

class Resistor(Component): 

    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode): 
        g = 1/self.num_value

        a = node_map.get(self.nodes[0])
        b = node_map.get(self.nodes[1])

        self.stamp_cell_a(a,a,g,matrix_a)
        self.stamp_cell_a(a,b,-g,matrix_a)
        self.stamp_cell_a(b,a,-g,matrix_a)
        self.stamp_cell_a(b,b,g,matrix_a)

    
    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode): 
            self.current = self.voltage/self.num_value
        
  
class Capacitor(Component): 
    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode): 
        if mode == "op": 
            pass 
          
        elif mode == "tran": 
            pass
    
    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode):
        if mode == "op": 
            self.current = 0 
       
        
        elif mode == "tran": 
            pass 
    
        
class Inductor(Component): 
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
            pass 


    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode): 
        if mode == "op": 
            index = extra_unknown_map[self.name]
            self.current = results_matrix[index][-1]
       

class VoltageSource(Component): 
    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode):

        a = node_map.get(self.nodes[0])
        b = node_map.get(self.nodes[1])
        c = extra_unknown_map.get(self.name)

        self.stamp_cell_a(a,c,1,matrix_a)
        self.stamp_cell_a(b,c,-1,matrix_a)
        self.stamp_cell_a(c,a,1,matrix_a)
        self.stamp_cell_a(c,b,-1,matrix_a)
        matrix_b[c] = self.num_value

    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode): 
        index = extra_unknown_map[self.name]
        self.current = results_matrix[index][-1]


class CurrentSource(Component): 
    def stamp(self,matrix_a,matrix_b,node_map,extra_unknown_map,mode):

        a = node_map.get(self.nodes[0])
        b = node_map.get(self.nodes[1])

        self.stamp_cell_b(a,-self.num_value,matrix_b)
        self.stamp_cell_b(b,self.num_value,matrix_b)

    def calcCurrent(self,results_matrix,node_map,extra_unknown_map,mode):
        self.current = self.num_value