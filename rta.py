##
## @author  Francesco Cervigni
## @date    2012-10
##
## This file contains the main logic of the application.
## The specific functions used are defined in separte files in the same folder.
##

from load import taskLoad
from analysis import DM_guarantee
import sys, operator

# START

if __name__ == '__main__':

    verbose = False
    print_worst = False


    if ( len (sys.argv) < 2 ) :
        print '\nSorry, wrong arguments. Please specify tasks file to load. (and nothing more)  \n\nUsage : \n\tpython main.py <task_file_path>\n'
        sys.exit(1)
    
    if ( len (sys.argv) == 3 ) :
        if sys.argv[1] == '-v':
            verbose = True
        if sys.argv[1] == '-w':
            print_worst = True
    
    if ( len (sys.argv) == 4 ) :
        if sys.argv[1] == '-v':
            verbose = True
        if sys.argv[1] == '-w':
            print_worst = True

    myTasks, myComs = taskLoad( sys.argv[len ( sys.argv ) - 1] )

    #for tas in myTasks : 
    #    tas.my_print()

    sche,res, desc= DM_guarantee( myTasks, verbose )

    #for t in myTasks :
    #    print t.my_print()
    #for c in myComs:
    #    c.my_print() 


    #print '\nGuarantee is:', sche 
    

    #print '\nResult : ', res
    print "\n-------------\nTASK\tWCRT\n-------------"
    for name, resp_time in sorted ( res.items(), reverse = False,  key=operator.itemgetter(1) ) :
        print "%s\t%s" % ( name , resp_time )
    print "-------------\n"
    
    if print_worst :
        print "\n-------------\nTASK\tWCRT\n-------------"
        for name, description in desc.items() :
            print "\n%s :\nInterference :\n%s" % ( name , description )
        print "-------------\n"
