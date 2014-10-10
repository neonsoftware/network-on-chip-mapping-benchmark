##
## @author  Francesco Cervigni
## @date    2012-10
##
## This file contains the main logic of the application.
## The specific functions used are defined in separte files in the same folder.
##

from data_structures import Mapping
from load import taskLoad
from analysis import DM_guarantee
import sys, operator, math
from copy import deepcopy

# START


def divide_routers (M, N):

    print '\n- Dividing routers in A_4, A_3, A_2'
    
    A_2 = []
    A_3 = []
    A_4 = []

    for index in range(M*N):
        #A2 are the coners, so 4
        if index == 0 or index == M -1 or index == M*(N-1) or index == (M*N-1) :
            A_2.append( ( index, None) )
        else :
            if index % M == 0 or index % M == M-1 or math.floor( index / M ) == 0 or math.floor( index / M ) == N-1 :
                A_3.append( ( index, None ) )
            else :
                A_4.append( ( index, None ) )
    print '\nSet\tTiles (indexes)'            
    print '------------------------------------------------'
    print 'A_4\t' , [ index for index, ob in A_4]    
    print 'A_3\t' ,[ index for index, ob in A_3]  
    print 'A_2\t' , [ index for index, ob in A_2]    

    return A_2, A_3, A_4


def assign_to_tiles( tasks_ordered , M, N, A_2, A_3, A_4) :

    print '\n- Mapping Tasks to tiles\n'

    mapping = Mapping (M, N)

    for task, level in tasks_ordered : 
       
        A_4_free = [ ( num, index ) for  num, (index, t) in enumerate(A_4) if t is None ]

        if len( A_4_free ) > 0  :

            print 'Placing ',  task.name, ' in on of the ', len( A_4_free ) , ' available slots in A4.'

            # If there is space in A_4
            best_cost = 100000000 
            best_index = -1
            best_num = -1

            # Deciding which is of the positions in A_4 is best
            for  ( num, index ) in A_4_free :

                mapping.set( task, index )
                
                if mapping.cost() < best_cost : 
                    best_index = index
                    best_cost = mapping.cost()
                    best_num = num

                mapping.set( None, index )    

            # Definitive mapping
            mapping.set( task, best_index )
       
            print 'Best A_4 tile for task ' , task.name , ' is ' , best_index,  ' :','\n', mapping                     
           
            # Updating A4
            A_4[best_num] = ( A_4[best_num][0], task ) 

        else:
          
            print 'Available slot in A3'

            A_3_free = [ ( num, index ) for  num, (index, t) in enumerate(A_3) if t is None ]
                
            if len( A_3_free ) > 0  :

                # If there is space in A_4
                best_cost = 100000000 
                best_index = -1
                best_num = -1

                # Deciding which is of the positions in A_4 is best
                for  ( num, index ) in A_3_free :

                    mapping.set( task, index )
                    
                    if mapping.cost() < best_cost : 
                        best_index = index
                        best_cost = mapping.cost()
                        best_num = num

                    mapping.set( None, index )    

                # Definitive mapping
                mapping.set( task, best_index )
           
                print 'Mapping task ' , task.name , ' to tile ' , best_index,  ' :','\n', mapping                     
               
                # Updating A4
                A_3[best_num] = ( A_3[best_num][0], task ) 
            else:
              
                print 'Available slot in A2'

                A_2_free = [ ( num, index ) for  num, (index, t) in enumerate(A_2) if t is None ]
                    
                if len( A_2_free ) > 0  :

                    # If there is space in A_4
                    best_cost = 100000000 
                    best_index = -1
                    best_num = -1

                    # Deciding which is of the positions in A_4 is best
                    for  ( num, index ) in A_2_free :

                        mapping.set( task, index )
                        
                        if mapping.cost() < best_cost : 
                            best_index = index
                            best_cost = mapping.cost()
                            best_num = num

                        mapping.set( None, index )    

                    # Definitive mapping
                    mapping.set( task, best_index )
               
                    print 'Mapping task ' , task.name , ' to tile ' , best_index,  ' :','\n', mapping                     
                    # Updating A4
                    A_2[best_num] = ( A_2[best_num][0], task ) 
        
    return mapping




def lcf_map ( tasks, M, N ):

    task_com = []

    for task in tasks : 
        
        count = 0

        for out in task.out_coms : 

            count += out.weight #todo see better this balance

        for in_com in task.in_coms : 

            count += in_com.weight #todo see better this balance

        task_com.append((task, count))

    task_com.sort(reverse = True, key=operator.itemgetter(1) ) 

    A_2, A_3, A_4 = divide_routers ( M, N ) 
    
    mapping = assign_to_tiles ( task_com , M, N, A_2, A_3, A_4 )

    print 'Final Mapping is - Cost ', mapping.cost(), '\n',  mapping, 



if __name__ == '__main__':

    verbose = False
    
    import argparse

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('file',help='Path of input file')
    parser.add_argument('-m','--lines', help='Tiles lines',type=int, required=True)
    parser.add_argument('-n','--columns', help='Tiles columns', type=int, required=True)
    parser.add_argument('-v', '--verbose', help='Verbose')
    args = vars(parser.parse_args())

    M = args['lines']
    N = args['columns']

    if  args['verbose'] is not None :
        verbose = True

    input_file = args['file']

    myTasks, myComs = taskLoad( input_file )

    if verbose : 
        print 'Tasks Loaded : '
        for t in myTasks :
            print t.my_print()
        print 'Communications loaded : '
        for c in myComs:
            c.my_print() 


    M = 5
    N = 5

    lcf_map(myTasks, M , N)    

