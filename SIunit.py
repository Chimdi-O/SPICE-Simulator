import sys


def SI_prefix(value): 
    
    unit_table = [ 
        [1e-15,"f"], 
        [1e-12,"p"], 
        [1e-9,"n"],
        [1e-6,"u"], 
        [1e-3,"m"], 
        [1,""],
        [1e3,"K"],
        [1e6,"Meg"], 
        [1e9,"G"],
        [1e12,"T"]]
    if value == 0:
        return "0"
    
    if abs(value) < unit_table[0][0]:
         return f"{value/unit_table[0][0]:.3g}" + unit_table[0][1]

    for i in range(len(unit_table)): 
        if abs(value) < unit_table[i][0]: 
            return f"{value/unit_table[i-1][0]:.3g}" + unit_table[i-1][1]
        
    return f"{value/unit_table[-1][0]:.3g}" + unit_table[-1][1]



def parseUnits(value): 
    i = len(value)-1 # a variable to track the start of the suffix 

    while i >= 0 and value[i].isalpha(): 
        i -= 1

    if  i == -1: 
        print(f"Error: Invalid value {value}")
        sys.exit()
    
    num = value[:i+1]
    unit = value[i+1:]    

    unit_table = {
        "t":1e12, 
        "g":1e9,
        "meg":1e6, 
        "k":1e3, 
        "":1, 
        "m":1e-3, 
        "u":1e-6, 
        "n":1e-9,
        "p":1e-12,
        "f":1e-15}
    
    if unit.lower() not in unit_table: 
        print(f"Error: Invalid unit {unit.lower}")
        sys.exit()

    return float(num) * unit_table[unit.lower()]