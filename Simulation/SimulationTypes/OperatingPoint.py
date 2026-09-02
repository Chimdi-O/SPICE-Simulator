from Simulation.MatrixMaths import buildMatrix, matrixSolver
from SIunit import SI_prefix


class OperatingPoint(): 
    def __init__(self,circuit,mode="op"): 
        self.circuit = circuit 
        self.results_matrix = [] 
        self.mode = mode 

    def run(self): 
        matrix = buildMatrix(self.circuit,self.mode)
        self.results_matrix = matrixSolver(matrix)
        self.circuit.parseResultsMatrix(self.results_matrix,self.mode)
        self.circuit.printValues() 


     

    
    