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
import sys, operator
from copy import deepcopy

# START


def generate_candidates_get_near( mapping, max_candidates, tabu_list ):
    '''
    This method iteraictively tries to resolve the higher distance
    '''

    print '\n- Generating', max_candidates, ' candidates :\n'
    
    candidates = [None]*  max_candidates

    first, second = mapping.max_distance_overall(tabu_list) 

    for index in  range ( max_candidates/2 ) :
        
        
        new_mapping = deepcopy(mapping)

        new_mapping.reduce_this_com( first, tabu_list )

        print '\nCandidate ', index, ' - cost ', new_mapping.cost(), ' :\n', new_mapping, '\n'

        candidates[index] = new_mapping 


    for index in  range ( max_candidates/2 ) :
        
        new_mapping = deepcopy( mapping) 

        new_mapping.reduce_this_com( second, tabu_list )

        print '\nCandidate ', index + max_candidates/2 , ' - cost ', new_mapping.cost(), ' :\n', new_mapping, '\n'

        candidates[index+max_candidates/2] = new_mapping 

    return candidates


def tabu_search( tasks, M, N, max_iter_times, max_candidates, max_tabu_list, verbose ):


    # Initializing with a random
    best_mapping = Mapping ( M, N)
    best_mapping.random_place( myTasks )
    #
    best_cost = best_mapping.cost()
    if verbose :
        print 'Initial mapping - Cost ', best_cost , ":\n", best_mapping
    #
    ########

    print '\n////// Tabu Search initialized with random mapping.'
    # Initializing tabu list
    tabu_list = []

    step = 0
    while ( step < max_iter_times  ):

        print '\n////// Global loop n.', step

        if ( step % 10 == 0 ):
            #
            # <<<<<<<<<<<<< HERE IS THE SPACE MOVEMENT, every 10 steps a new random mapping is produced,
            # this way the global loop 'explores'
            #
            # Generating candidates (neighbors)
            m = Mapping(M,N)
            m.random_place( myTasks )
            candidates = generate_candidates_get_near( m , max_candidates, tabu_list ) 
        else:
            # Generating candidates (neighbors)
            candidates = generate_candidates_get_near( best_mapping, max_candidates, tabu_list ) 


        # Choosing the best candidates
        if verbose : 
            print 'The cost of the sorted is ', [ c for x, c in sorted( [ (mapping, int(mapping.cost())) for mapping in candidates] , key=operator.itemgetter(1) ) ]
        
        best_candidate = sorted( [ (mapping,int( mapping.cost())) for mapping in candidates],  key=operator.itemgetter(1) )[0][0]

        print '- Best Local candidate has cost ', best_candidate.cost(), ' and is :\n', best_candidate  

        if best_candidate.cost( ) < best_cost : 

            print '\n>>>>>>>>>>>> Best Local candidate has had become Best Global Candidate ! \n'
            # Updating the tabu list
            print '\nUpdating Tabu List\n'
            tabu_list.append( [ i for i, j in zip(best_mapping.tiles,best_candidate.tiles) if i!=j and i is not None ] ) 

            best_mapping = best_candidate
            best_cost = best_mapping.cost()
            
            if verbose : 
                print '--- New best is - Cost : ', best_candidate.cost() , '\n',   best_candidate, '\n'

            # Keeping the list "fresh" 
            while len( tabu_list ) > max_tabu_list : 

                tabu_list.pop(0)

        step += 1

    return best_mapping



if __name__ == '__main__':

    verbose = False

    import argparse

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('file',help='Path of input file')
    parser.add_argument('-m','--lines', help='Tiles lines',type=int, required=True)
    parser.add_argument('-n','--columns', help='Tiles columns', type=int, required=True)
    parser.add_argument('-v','--verbose', help='Verbose')
    parser.add_argument('--size_tabu', help='Size of the tabu list', type=int, required=True)
    parser.add_argument('--global_loops', help='Number of global loops', type=int, required=True)
    parser.add_argument('--num_candidates', help='Number of candidates per internal loop', type=int, required=True)
    args = vars(parser.parse_args())

    M = args['lines']
    N = args['columns']
    size_tabu       = args['size_tabu']
    global_loops    = args['global_loops']
    num_candidates  = args['num_candidates']

    if  args['verbose'] is not None :
        verbose = True

    input_file = args['file']

    if num_candidates % 2 != 0 :
        print '\n\nERROR ! num_candidates *must* be even. Please :)\n\n'
        sys.exit(1)

    myTasks, myComs = taskLoad( input_file )

    if verbose : 
        print 'Tasks Loaded : '
        for t in myTasks :
            print t.my_print()
        print 'Communications loaded : '
        for c in myComs:
            c.my_print() 

    best_mapping = tabu_search ( myTasks, M , N, global_loops , num_candidates , size_tabu, verbose)


    print '\nResult - Cost ',best_mapping.cost() , "\n",  best_mapping

