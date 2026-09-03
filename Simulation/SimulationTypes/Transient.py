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
            print(time)
            for component in self.circuit.components: 
                if component.name[0] == "C" or component.name[0] == "L": 
                    component.update_companion_models(self.time_step)

            matrix = buildMatrix(self.circuit,"tran")
            self.results_matrix = matrixSolver(matrix)
            self.circuit.parseResultsMatrix(self.results_matrix,"tran")
           
            self.store_results(time)

            if ( time + self.time_step ) > self.stop_time: 

                time = self.stop_time 
                print(time)
                for component in self.circuit.components: 
                                if component.name[0] == "C" or component.name[0] == "L": 
                                    component.update_companion_models(self.time_step)
                
                matrix = buildMatrix(self.circuit,"tran")
                self.results_matrix = matrixSolver(matrix)
                self.circuit.parseResultsMatrix(self.results_matrix,"tran")
                self.store_results(time)
                

            time += self.time_step
        
        self.plot()
       

    def store_results(self,time): 
        self.results["time"].append(time)
        self.results["voltage"].append(self.circuit.voltages)
        self.results["current"].append(self.circuit.currents)

    def query_plot_variable(self): 
         
         print("[V]oltage, [C]urrent or [Q]uit")
         quanitity = input("choose a quantity:    ")
         print()

         if quanitity == "Q":  
              return "Quit"
        
         if quanitity == "C": 
            
            print(self.circuit.component_map)
            target = input("Enter a component current to be plotted:   ")
            print()

            if target  in self.circuit.component_map: 
                 target = self.circuit.component_map[target]
                 return ["current",target]
                 
            else: 
                 print("Invalid component\n")
                 return None 
                 
                 
         if quanitity == "V": 

            print(self.circuit.node_map)
            target = input("Enter a node voltage to be plotted:   ")
            print()

            if target in self.circuit.node_map: 
                 target = self.circuit.node_map[target]
                 return ["voltage",target]

            else:
                print("Invalid node\n")
                return None

         else: 
              print("Invalid quantity\n")
              return None 
                    

    def plot(self): 

        plot_variable = self.query_plot_variable()
        while plot_variable != "Quit":
            if plot_variable and plot_variable != "Quit": 
                plot_values = [] 
                for i in self.results[plot_variable[0]]: 
                    plot_values.append(i[plot_variable[1]])
                

            
            
                plt.plot(self.results["time"], plot_values)
                plt.show()
            plot_variable = self.query_plot_variable()

        
         

             

