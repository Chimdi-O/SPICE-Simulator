from Simulation.MatrixMaths import buildMatrix, matrixSolver
from SIunit import SI_prefix
import matplotlib.pyplot as plt


class Transient(): 
    def __init__(self,circuit,time_step,stop_time): 
        self.circuit = circuit 
        self.results_matrix = [] 
        self.time_step = time_step
        self.stop_time = stop_time 
        self.results = { "time":[], "voltage":[], "current":[]}

    def run(self): 

        time = 0 

        while time < self.stop_time: 
            for component in self.circuit.components: 
                if component.name[0] == "C" or component.name[0] == "L": 
                    component.update_companion_models(self.time_step)

            matrix = buildMatrix(self.circuit,"tran")
            self.results_matrix = matrixSolver(matrix)
            self.circuit.parseResultsMatrix(self.results_matrix,"tran")
           
            self.store_results(time)

            if ( time + self.time_step ) > self.stop_time: 

                time = self.stop_time 

                for component in self.circuit.components: 
                                if component.name[0] == "C" or component.name[0] == "L": 
                                    component.update_companion_models(self.time_step)
                
                matrix = buildMatrix(self.circuit,"tran")
                self.results_matrix = matrixSolver(matrix)
                self.circuit.parseResultsMatrix(self.results_matrix,"tran")
                self.store_results(time)
                

            time += self.time_step
        print(self.results)
        self.plot("voltage",'2')
       

    def store_results(self,time): 
        self.results["time"].append(time)
        self.results["voltage"].append(self.circuit.voltages)
        self.results["current"].append(self.circuit.currents)

    def plot(self,quanitity,target): 
         

         if quanitity == "voltage": 
              print(quanitity)
              index = self.circuit.node_map[target]
              target_voltages = []

              for i in self.results["voltage"]: 
                   target_voltages.append(i[index])
              print("to!")
              plt.plot(self.results["time"], target_voltages)
              plt.show()

         
         if quanitity == "current": 
              index = self.circuit.component_map[target]
              target_currents = [] 

              for i in self.results["current"]: 
                    target_currents.append(i[index])

              plt.plot(self.results["time"], target_currents)
              plt.show()


        
         

             

