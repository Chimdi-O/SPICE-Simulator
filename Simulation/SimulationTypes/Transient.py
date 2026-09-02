from Simulation.MatrixMaths import buildMatrix, matrixSolver
from SIunit import SI_prefix


class Transient(): 
    def __init__(self,circuit,time_step,stop_time): 
        self.circuit = circuit 
        self.results_matrix = [] 
        self.time_step = time_step
        self.stop_time = stop_time
        self.results = { "time":[], "votlage":[], "current":[]}

    def run(self): 

        time = 0 

        while time < self.stop_time: 
            for component in self.circuit.components: 
                if component.name[0] == "C" or component.name[0] == "L": 
                    component.update_companion_models(self.time_step)

            matrix = buildMatrix(self.circuit,"tran",self.time_step)
            self.results_matrix = matrixSolver(matrix)
            self.circuit.parseResultsMatrix(self.results_matrix)
                                               

             



     # while time < stop_time -> time +time_step
     # update companion models 
     # solve
     # calculate currents and what not 
     # store everything 
     #start again! 


            #
            # self.circuit.printValues() 