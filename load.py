##
## @author  Francesco Cervigni
## @date    2012-10
##
## The function 'load' :
##   - loads the tasks
##   - prints the tasks, including their attributes
##   - returns a list of instances of class Task
##


from data_structures import Task, Com
from xml.dom import minidom


## Loading File

def taskLoad( file_name ):

    xmldoc = minidom.parse( file_name )
    nodeslist = xmldoc.getElementsByTagName('node') 
    edgeslist = xmldoc.getElementsByTagName('edge') 


    #print len(itemlist)
    #print itemlist[0].attributes['Name'].value

    tasks = []

    coms = []

    #### LOADING

    for s in nodeslist :
        n = Task ( s.attributes['id'].value, 
                    s.attributes['Name'].value,
                    s.attributes['WCET'].value,
                    s.attributes['BCET'].value,
                    s.attributes['Period'].value,
                    s.attributes['Deadline'].value,
                    s.attributes['Priority'].value)

        tasks.append( n )

    for e in edgeslist : 
        c = Com ( e.attributes['id'].value,
                 e.attributes['source'].value,
                 e.attributes['target'].value, 
                 e.attributes['weight'].value, 
                 tasks )

        coms.append(c)

    return tasks, coms

