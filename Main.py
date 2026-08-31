from Interpreter import Interpreter

# fix the voltage source stamping thing
# make an error message for a shit spice file e.g disconnected nodes 

file = "SpiceTest.txt"


interpreter = Interpreter()
interpreter.parseFile(file)
# for current 

interpreter.simulation_manager.runDirectives()



