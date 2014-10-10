import math, random

class Task( object ):
    """A task"""
    def __init__(self,
                  Id                  ,
                  Name                ,
                  WCET                ,
                  BCET                ,
                  Period              ,
                  Deadline            ,
                  Priority                 ):
        self.id       = str(Id) 
        self.name     = str(Name)
        self.wcet     = int(WCET)
        self.bcet     = int(BCET)
        self.period   = int(Period)
        self.deadline = int(Deadline)
        self.priority = int(Priority)
        self.in_coms  = [ ] 
        self.out_coms = [ ]

    def my_print (self):
        print '\n////// Task ',  self.id
        print 'Name     : ' + self.name
        print 'WCET     : %d ' % self.wcet
        print 'BCET     : %d ' % self.bcet
        print 'Period   : %d ' % self.period
        print 'Deadline : %d ' % self.deadline
        print 'Priority : %d ' % self.priority
        print 'in_coms    : ', [ " <--" + str(s.weight) + "-- " + s.source.name for s in self.in_coms ]
        print 'out_coms   : ', [ " --" + str(s.weight) + "--> " + s.destination.name for s in self.out_coms ]
        print '///////////////\n'

class Com( object ):
    """A communication between a task and another"""
    def __init__(self,
                  Id                  ,
                  source              ,
                  destination         ,
                  weight              ,
                  tasks                 ):

        self.id             = str(Id) 
        self.weight         = int (weight)
        
        for t in tasks : 
            if t.id == source :
                t.out_coms.append( self )
                self.source   = t
            if t.id == destination :
                t.in_coms.append( self )
                self.destination   = t

    def my_print (self):
        print '\n////// Communication '
        print self.id + " : " + self.source.name + '--'+ str(self.weight) + '-->' + self.destination.name
        print '///////////////\n'
    

class Mapping( object ) :
    ''' 
    Defines a mapping of t Tasks in an NxM 2D mesh
    This object includes the mesh
    '''
    def __init__( self, N, M ):

            self.N = N
            self.M = M
            
            self.tiles = [None] * (N*M)

    def get_pos ( self, task ) :
        
        for index in range(len(self.tiles)) :
            if self.tiles[index] is not None and self.tiles[index].name == task.name :
                return math.floor( index / self.N ), index % self.N
        
        return None, None
   
    def set_with_coord ( self, task, x, y ):

        self.tiles[ x * self.N  + y] = task
    
    def set ( self, task, index ):
        
        self.tiles[ index  ] = task

    def get ( self, x, y ):
        
        return self.tiles[ x * self.N  + y]

    def manhattan_distance( self, x1, y1, x2, y2 ):
        '''
        Computes the manhattan distance.
        between the points (x1,y1) and (x2,y2)
        on a 2D plane
        '''

        return ( abs(x1-x2) + abs(y1-y2) )


    def manhattan_distance( self, task1, task2 ):
        '''
        Computes the manhattan distance between two tasks
        on a 2D plane
        '''

        x1, y1 = self.get_pos( task1 )

        x2, y2 = self.get_pos( task2 )

        return ( abs(x1-x2) + abs(y1-y2) )

    def tasks(self) :

        return [ t for t in self.tiles if t is not None ] 

    def random_place( self, tasks ):

        for t in tasks :

            done = False

            while ( not done ) :

                x = random.randint(0, self.M-1) 
                y = random.randint(0, self.N-1) 

                if ( self.get(x,y) == None) :

                    self.set_with_coord( t , x, y)
                    done = True

    def __repr__(self) :

        string = ''

        for x in range(self.N) :
            
            string += '|'
            
            for y in range(self.M) :

                elem = self.get(x,y)

                if elem is None :
                    string += "   X" + '\t|'
                else:
                    string += "   " + self.get(x,y).name + '\t|'
            
            string += '\t\n'

        string += '\n'
        return string

    def cost ( self ):

        cost = 0 

        for x in range(self.N) :
            for y in range(self.M) :
                elem = self.get(x,y)

                if elem is not None : 

                    for out in elem.out_coms :

                        dest = out.destination
    
                        dest_x, dest_y = self.get_pos(dest)

                        if ( dest_x is not None) : # todo, this is jus tfor LFC
                            cost += out.weight * self.manhattan_distance( elem, dest )

                        #print 'Adding distance between' + elem.name + ' and ' + dest.name

        return cost

    def max_distance_lenght ( self ):

        max_com = 0 

        for x in range(self.N) :
            for y in range(self.M) :

                elem = self.get(x,y)

                if elem is not None : 

                    for out in elem.out_coms :
                        
                        if not ( (out.source in tabu_list) and (out.destination in tabu_list) ) :

                            dest = out.destination

                            new_dist = self.manhattan_distance( elem, dest )

                            if new_dist  > max_com:
                                
                                second_max_com = max_com 
                                max_com = out

                            else : 
                                if new_dist > second_max_com :
                                    second_max_com = out

        return max_com, second_max_com

    def max_distance_overall ( self, tabu_list):

        max_com = 0 
        second_max_com = 0 

        for x in range(self.N) :
            for y in range(self.M) :

                elem = self.get(x,y)

                if elem is not None : 

                    for out in elem.out_coms :

                        if not ( (out.source in tabu_list) and (out.destination in tabu_list) ) :
                            dest = out.destination

                            new_dist = out.weight * self.manhattan_distance( elem, dest )

                            if new_dist  > max_com:
                                
                                second_max_com = max_com 
                                max_com = out
                            else : 
                                if new_dist > second_max_com :
                                    second_max_com = out

        return max_com, second_max_com

    def reduce_this_com( self, com, tabu_list  ):

        if (not com.source in tabu_list):
            to_move = com.source
            other = com.destination
        else : 
            # By specification of max_com_...  either source or destination is assumet to not be in the tabu list
            to_move = com.destination
            other = com.source
        
        if not to_move in tabu_list :

            to_move_x, to_move_y = self.get_pos(to_move)
            to_move_index = int(to_move_x) * self.N + int(to_move_y)

            # Trying to change the source
            possible = [None]*4

            # Possibility on the right
            possible[0]= [ i for i in range(len(self.tiles)) if i > to_move_index and (not self.tiles[i] in tabu_list ) and ( self.tiles[i] is not other)  ]

            # Possibility on the left
            possible[1]= [ i for i in range(len(self.tiles)) if i < to_move_index and (not self.tiles[i] in tabu_list ) and ( self.tiles[i] is not other)  ]
           

            # Possibility on above on y axis
            possible[2]= [ i for i in range(len(self.tiles)) if i < (to_move_index - self.N) and (not self.tiles[i] in tabu_list ) and ( self.tiles[i] is not other)  ]
            

            # Possibility on below on y axis
            possible[3]= [ i for i in range(len(self.tiles)) if i > (to_move_index + self.N) and (not self.tiles[i] in tabu_list ) and ( self.tiles[i] is not other)  ]

            
            direction = random.randint(0, 3)
            
            while ( len ( possible[direction] ) <= 0 ):
                direction = random.randint(0, 3)
            
            
            point = random.randint(0, 2)
           
            while point >= len( possible[direction] ) :
                point = random.randint(0, 2)


            index_for_swap = possible[direction][point] 

            direction_string = ["->", "<-", "^", "v"] 

            print 'Swap : direction : ' , direction_string[direction], ', swapping ', to_move_index, ' with ', index_for_swap
           
            self.tiles[to_move_index] = self.tiles[index_for_swap]
            self.tiles[index_for_swap] = to_move



