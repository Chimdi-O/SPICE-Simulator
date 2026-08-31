
class SimulationManager(): 
    def __init__(self,circuit): 
        self.directives = [] 
        self.circuit = circuit 

    def runDirectives(self): 
        for directive in self.directives: 
            self.runDirective(directive)
    
    def runDirective(self,directive): 
        directive.run() 
        


        
        

