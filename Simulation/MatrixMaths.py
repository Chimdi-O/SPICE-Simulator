
def buildMatrix(Circuit,mode): 
    
    extra_unknowns = ["V"]

    if mode == "op": 
          extra_unknowns.append("L")

    for component in Circuit.components: 
        if component.name[0] in extra_unknowns: 
             Circuit.extra_unknown_map[component.name] = len(Circuit.node_map) + len(Circuit.extra_unknown_map) 

    n = len(Circuit.node_map)+len(Circuit.extra_unknown_map)
    matrix_a = [[0 for _ in range(n)] for _ in range(n)]
    matrix_b = [0 for _ in range(n)]
  
    for component in Circuit.components: 
         matrix = component.stamp(matrix_a,matrix_b,Circuit.node_map,Circuit.extra_unknown_map,mode)
    

    aug_matrix = matrix_a

    for i in range(n): 
         aug_matrix[i].append(matrix_b[i])

    print(aug_matrix)
    return aug_matrix
            


#there are only comments here bc the rest of the program is straightforward and self explanatory
#NOTE if there is a row of zeros that is a singular matrix and it cannot be solved!!!!

def matrixSolver(matrix):

    #these two identify the index of the pivot 
    current_column = 0
    current_row = 0 


    # guass part (make all the cells below each pivot zero to create a "triangle of zeros")
    while current_column < len(matrix[0])-1: # why?? 

        #This chooses the first non zero item in the current column as the pivot and moves it row its a part of to the current row
        for a in range(current_row,len(matrix)): 
            if matrix[a][current_column] != 0: 
                temp = matrix[a]
                matrix[a] = matrix[current_row]
                matrix[current_row] = temp
                break
        
        #really should be called pivot instead of first value, stores pivot
        first_value  = matrix[current_row][current_column]

        #scales the current row down by first value to make the pivot 1         
        for a in range(len(matrix[current_row])):
            matrix[current_row][a] = matrix[current_row][a]/first_value

        # goes through each row making the numbers below the pivot 0 
        for a in range(current_row+1,len(matrix)):

            # finds the scaling factor by finding the amount the pivot would need to scale to match the number in a row below the pivot
            factor = -1 * matrix[a][current_column]/matrix[current_row][current_column]

            #adds the current row to scaled to one of the rows below to make the number under the pivot zero
            for b in range(len(matrix[current_row])): 
                matrix[a][b] += factor * matrix[current_row][b]

        #moves onto the next pivot which is diagonally down from the previous one 
        current_column += 1 
        current_row += 1 

        
    # jordan part (Make it an idenity matrix)
    # since current column increments at the end of the list after the guass part it will be addressing outside of the matrix 
    current_column -= 1 
    current_row -= 1 

    # start at the lowest pivot and make the numbers above it in each row zero then go onto the next pivot
    for a in reversed(range(1,len(matrix))):
        for b in range(0,current_row): 

            # the factor we have to increase by the make a number above the pivot zero is just the number since now al the pivots are one
            factor = -1*matrix[b][current_column]
            
            #take away (add) the rows scaled by the factor
            for c in range(len(matrix[0])): 
                matrix[b][c] += matrix[current_row][c]*factor 
        
        # move to the next pivot and repeat 
        current_column -= 1 
        current_row -= 1

    print(matrix)
    return matrix