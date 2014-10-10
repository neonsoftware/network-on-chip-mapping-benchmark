from task import Task 

import math

def sum_other_inters ( t, time, resp, task_set ) :
    
    inter = 0

    description = ''

    for task in task_set : 
        if ( task is not t ) and ( task.priority < t.priority )  : 
            inter += ( math.ceil( float(resp) / task.period ) * task.wcet )
            description += '\ntask ' + task.name + ' has done preemption ' + str( math.ceil( float(resp) / task.period ) ) + ' times, running ' + str(task.wcet) + ' each'

    return inter, description

def DM_guarantee( task_set, verbose ):

    results = {}

    is_schedulable = False

    desc = {}
    
    for t in task_set :
       
        inter = 0
        description = 'No Interference'
        time = 0

        # To transform the while in a do-while
        again = True  

        while ( again ) :

            resp = inter + t.wcet
    

            if verbose : 
                t.my_print()
                print '\t\tInter : %d' % inter
                print '\t\tResp : %d' % resp
                print '\t\tWcet : %d' % t.wcet
                print '\t\tTime : %d' % time
                print '\t\tDeadline : %d' % t.deadline
            
            #print '- ' + str(t.id) + ' has now resp ', resp

            
            if ( resp > t.deadline ) :
                results[t.name]= 'no' 
                desc[t.name] = description
                print '- ' + str(t.id) + ' non schedulable'
                #print '- ' + str(t.id) + ' has now resp ', resp
                break

            inter, description = sum_other_inters ( t, time, resp, task_set )

            # Assign to boolean variable
            # It is a bit ugly, but python supports it
            again = ( inter + t.wcet > resp )

            if verbose : 
                print '\t\tNew inter : %d\n' % inter

            if again :
                
                if verbose :
                    print '\t\tinter + t.wcet > resp '
            else:
                
                results[ t.name ] = int(resp)
                desc[ t.name ] = description

                
                if verbose :
                    print str(t.id) + ' IS schedulable !!!!'
                
                break


            time = time + 1




    return (is_schedulable, results, desc)


