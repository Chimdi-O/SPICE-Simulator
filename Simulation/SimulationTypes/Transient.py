from Simulation.MatrixMaths import buildMatrix, matrixSolver
from SIunit import SI_prefix
import matplotlib.pyplot as plt
import sys 
from Circuit.Components import Diode


class Transient(): 
    def __init__(self,circuit,time_step,stop_time): 
        self.circuit = circuit 
        self.results_matrix = [] 
        self.time_step = time_step
        self.stop_time = stop_time 
        self.time = 0 
        self.results = { "time":[], "voltage":[], "current":[]}

    def run_time_step(self,time_step):
        if self.time == 0: 
            print("0%")
        else: 
            print( round(100*(self.time/self.stop_time),3),"%")
    
        for component in self.circuit.components: 
            if component.ac:  
                component.update(self.time_step,self.time)




        if self.circuit.hasDiodes(): 
            self.newtonRaphson() 

        else: 
            self.solve() 

        self.store_results(self.time) 
        self.time += time_step

    def solve(self): 
        matrix = buildMatrix(self.circuit,"tran")
        self.results_matrix = matrixSolver(matrix)
        self.circuit.parseResultsMatrix(self.results_matrix,"tran")



    def newtonRaphson(self): 
        converged = False 

        old_voltages = [0.0] * len(self.circuit.node_map)
        iteration = 1 

        while converged == False:
            if iteration == 50: 
                print("Error: Newton Raphson did not converge")
                sys.exit() 

            for component in self.circuit.components: 
                if isinstance(component,Diode): 
                    component.update()
            self.solve() 
            new_voltages = self.circuit.voltages.copy()

            converged = self.checkConvergence(old_voltages,new_voltages)

            old_voltages = new_voltages.copy() 

            iteration += 1 



    def checkConvergence(self,old_voltages,new_voltages): 
        max_change = 0

        for i in range(len(old_voltages)):
            change =  abs(old_voltages[i] - new_voltages[i])

            if change > max_change: 
                max_change = change 

        if max_change < 1e-4: 
            return True 
        else: 
            return False 
         

    def run(self): 
        while self.time < self.stop_time: 
            self.run_time_step(self.time_step)

            if ( self.time + self.time_step ) > self.stop_time: 
                time_step = self.stop_time - self.time 
                self.run_time_step(time_step)

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
            
            print(", ".join(str(k) for k in self.circuit.component_map))
            target = input("Enter a component current to be plotted:   ")
            print()

            if target  in self.circuit.component_map: 
                 target = self.circuit.component_map[target]
                 return ["current",target]
                 
            else: 
                 print("Invalid component\n")
                 return None 
                 
                 
         if quanitity == "V": 

            print(", ".join(str(k) for k in self.circuit.node_map))
          
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

        
         

             

