from Simulation.MatrixMaths import buildMatrix, matrixSolver
from SIunit import SI_prefix
from Circuit.Components import Diode 
import sys


class OperatingPoint(): 
    def __init__(self,circuit,mode="op"): 
        self.circuit = circuit 
        self.results_matrix = [] 
        self.mode = mode 


    def solve(self): 
        matrix = buildMatrix(self.circuit,self.mode)
        self.results_matrix = matrixSolver(matrix)
        self.circuit.parseResultsMatrix(self.results_matrix,self.mode)


    def newtonRaphson(self): 
        converged = False 

        old_voltages = [0.0] * len(self.circuit.node_map)
        iteration = 1 

        while converged == False:
            if iteration == 500: 
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

        if self.circuit.hasDiodes(): 
                self.newtonRaphson() 

        else: 
            self.solve() 
    
        self.circuit.printValues() 
    

        


     

    
    