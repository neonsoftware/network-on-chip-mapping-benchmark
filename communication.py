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
import sys

# START

if __name__ == '__main__':

    verbose = False

    if ( len (sys.argv) < 2 ) :
        print '\nSorry, wrong arguments. Please specify tasks file to load. (and nothing more)  \n\nUsage : \n\tpython main.py <task_file_path>\n'
        sys.exit(1)
    
    if ( len (sys.argv) == 3 ) :
        if sys.argv[1] == '-v':
            verbose = True

    myTasks, myComs = taskLoad( sys.argv[len ( sys.argv ) - 1] )

    m = Mapping ( 5, 5)

    print m

    m.random_place( myTasks )

    print m

    print 'Cost : ' + str( m.cost() )

    #for tas in myTasks : 
    #    tas.my_print()

    sche,res = DM_guarantee( myTasks, verbose )

    for t in myTasks :
        print t.my_print()
    for c in myComs:
        c.my_print() 


    print '\nGuarantee is:', sche 
    

    print '\nResult : ', res
    print "\n-------------\nTASK\tWCRT\n-------------"
    for name, resp_time in res.items() :
        print "%s\t%s" % ( name , resp_time )
    print "-------------\n"
