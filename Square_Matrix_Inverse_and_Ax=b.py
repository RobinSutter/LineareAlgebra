#takes the useres input, let him choose between solving a system of eqution or just calc. the inverse
# prints error messages if input isn't valid
def input_matrix():
    matrix = []
    vector_b = []
    answer = input('Do you want to calculate the solution of a system of equation? Or just calculate the inverse?    (1  for system of equation)    (2  for only the inverse) ') 

    if answer == '1':
        solve_system = True
    elif answer == '2':
        solve_system = False
    else:
        print('Invalid input')
        exit(1)

    # asks which dimension it should have ( 3x3 or 4x4)
    matrix_size = int(input('Which dimension will your square matrix have? As input, give the amount of rows: '))
    if matrix_size <= 0:
        print('The dimension of your matrix is not valid')
        exit(1)
    # asks for every element of matrix depending on the choosen size
    for i in range (matrix_size):
        matrix.append([])
    try:
        for i in range (matrix_size):
            for j in range(matrix_size):
                matrix[i].append(float(input(f'Element at Index {i+1}{j+1}: ')))
    # asks if it was choosen to solve a system of equation
        if solve_system:
            for i in range (matrix_size):
                vector_b.append(float(input(f'b{i+1}: ')))
    except ValueError:
        print('---------------------')
        print('Error: Invalid Input')
        exit(1)
        
    return matrix, matrix_size,solve_system,vector_b 

# checks if a given matrix is invertible or not by testing if its rowreduced form is the identity matrix
def check_if_invertible(matrix,matrix_size,solve_system):
    matrix_copy = []
    counter = 0
    #need to make a copy of the  matrix so the original matrix does not get changed
    for element in matrix:
        matrix_copy.append([])
        for entry in element:
            matrix_copy[counter].append(entry)
        counter += 1
    #cheks if reduced matrix is row reduced
    try:
        matrix_copy = row_reducing(matrix_copy, matrix_size)
        matrix_copy = float_error_and_rounding(matrix_copy,matrix_size,solve_system)
        for i in range (matrix_size):
            counter = 0
            for j in range (matrix_size):
                if counter == i:
                    if matrix_copy[i][j]!= 1:
                        raise ValueError('Error: The provided Matrix is singular')
                elif matrix_copy[i][j]!= 0:
                    raise ValueError('Error: The provided Matrix is singular')
                counter += 1


    except ValueError as error:
        print('---------------------')
        print (error)
        exit(1)


def augmented_matrix(matrix,matrix_size):
    for i in range (matrix_size):
        counter = 0
        for j in range (matrix_size):
            if counter == i:
                matrix[i].append(1)
            else:
                matrix[i].append(0)
            counter += 1
    return matrix


# row reduces a given matrix ( sqaure matrix) 
def row_reducing(matrix, matrix_size):
    row_pivot = 0
    column_pivot = 0 
    row = 0
    column_entry = 0
    for i in range (matrix_size):
        if matrix[row_pivot][column_pivot] == 0:
            # sorts matrix so that the pivot element isn't 0, takes abs because -7 should be above 0 ...
            matrix.sort(key=lambda inner_list: [abs(element) for element in inner_list],reverse = True) 
            if matrix[row_pivot][column_pivot] == 0:
                raise ValueError('Error: The provided Matrix is singular')

        if matrix[row_pivot][column_pivot] != 1:
            devider = matrix[row_pivot][column_pivot]
            for element in matrix[row_pivot]: # makes that pivot entry is = 1 and the other elments in that row are devided by same number
                matrix[row_pivot][column_entry] = element/devider
                column_entry +=1
            column_entry = 0 
        
        row = row_pivot #get current row of pivot
            # make all zeroes under the pivot
        for i in range (matrix_size-1-row_pivot): # only for the amount of entries below the pivot
            row += 1 # as one wants to check for the next rows  under pivot
            if matrix[row][column_pivot]!= 0: 
                subtract_number = matrix[row][column_pivot] # get the number which should be 0
                for element in matrix[row]:
                    matrix[row][column_entry] = element - (subtract_number*(matrix[row_pivot][column_entry])) # subtract n-times(pivot row) from the rov as the entry should get 0
                    column_entry += 1

                column_entry = 0

        # make all zeroes above pivot
        if row_pivot !=0:
            for i in range(1,(row_pivot+1)):
                subtract_number = matrix[row_pivot-i][column_pivot]
                if subtract_number !=0: # if number above pivot is not 0
                    for element in matrix[row_pivot-i]:
                        matrix[row_pivot-i][column_entry]= element - (subtract_number*(matrix[row_pivot][column_entry]))
                        column_entry+= 1

                    column_entry = 0      
        row_pivot += 1
        column_pivot += 1

    return matrix

# makes that every -0.0 is replaced by 0 (doesn't affect anything but looks nicer with just 0)
def float_error_and_rounding(matrix,matrix_size,solve_system):
    for i in range (matrix_size):
        index = 0
        for element in matrix[i]:
            if element == 0:
                matrix[i][index] = 0
            elif solve_system==False:
                matrix[i][index] = round(matrix[i][index],2)
            index+= 1 
    return matrix

# get rid of the identity matrix
def only_inverse_rounded(matrix,matrix_size,solve_system):
    for i in range (matrix_size):
        for j in range (matrix_size):
            del matrix[i][0]
    matrix = float_error_and_rounding(matrix,matrix_size,solve_system)
    return matrix

#prints original matrix
def print_original(matrix,matrix_size):
    print()
    print('That is your provided Matrix A:')
    print()
    for i in range (matrix_size):
        print(matrix[i])
    print()

# prints right hand side
def print_right_side(vector_b,matrix_size):
    print('That is the provided right-handside b:')
    print()
    for i in range (matrix_size):
        print(f'b{i+1}: {vector_b[i]}')

#prints matrix in a nicer way
def print_matrix(matrix,matrix_size):
    print()
    print('That is the Inverse of the provided Matrix A:')
    print()
    for i in range (matrix_size):
        print(matrix[i])
    print()

#multiply inverse and vecotr b to get the solutions
def multiplication(matrix_inverse,vector_b,matrix_size):
    result_x = []
    for i in range(matrix_size):
        not_final_result = 0
        for j in range (matrix_size):
            not_final_result += (matrix_inverse[i][j] * vector_b[j])
        result_x.append(not_final_result)
    return result_x
        
# prints solution of ax =b          
def print_solution(result_x):
    print()
    print('The solution for the given Ax=b is:')
    print()
    count = 1
    for elements in result_x:
        print(f'x{count} = {elements:.2f}')
        count += 1

#start of programm  
def main():

    matrix, matrix_size,solve_system,vector_b  = input_matrix()
    
    print_original(matrix,matrix_size)
    
    # only if we have to solve system of equation
    if solve_system:
        print_right_side(vector_b,matrix_size)

    check_if_invertible(matrix,matrix_size,solve_system)

    matrix = augmented_matrix(matrix,matrix_size)

    matrix = row_reducing(matrix, matrix_size) 

    matrix_inverse = only_inverse_rounded(matrix,matrix_size,solve_system)

    if not solve_system:
        print_matrix(matrix_inverse,matrix_size)
    else:
        result_x = multiplication(matrix_inverse,vector_b,matrix_size)
        print_solution(result_x)


if __name__ == '__main__':
    main()