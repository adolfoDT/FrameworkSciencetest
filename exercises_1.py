__author__ = 'Adolfo Diaz Taracena'
__version__ = '1.0'
__all__ = ['Exercise 1',
           'Triple_Number']


def triple_number_iterative(n,numbers):
    
    if n == 1:
        result = numbers[0]
    elif n == 2:
        result = numbers[0]
    elif n == 3:
        result = numbers[2]
    elif n > 3:
        for i in range(2, n - 1):
            contador = numbers[i] + numbers[i - 1] + numbers[i - 2]
            numbers.append(contador) 
        total = len(numbers)
        result = numbers[total-1]

    return result


# def triple_number_recursive(n,numbers):
    
#     if n > 3:
#         contador = numbers[len(numbers)-1] + numbers[len(numbers)-2] + numbers[len(numbers)-3]
#         numbers.append(contador)


#         return triple_number_recursive(n-1, numbers)

#     if n == 3:
#         print(numbers[len(numbers) - 1])
#         return
      
#     elif n == 1:
#         print(2)


#     elif n == 2:
#         print(2)
    
 
    
# i didn´t do the recursive code it´s not working well
# for run the code just write : python  exercercise_2.py
if __name__ == "__main__": 
    numbers = [2, 2, 3]
    n = int(input("Insert a number: "))
    type_of_function = int(input("""Select a number for choose the type of function:
        1.- Iterative function :
     """))
    if type_of_function == 1:
        print("You select Iterative function")
        insert_numbers = triple_number_iterative(n, numbers)
        print("The result is : {}".format(insert_numbers))
    else:
        print("You have to choose 1")

    
