'''
Created on Jul 26, 2015

@author: J. Sanchez-Garcia
'''

import logging
logger = logging.getLogger(__name__)

def parser_wml(file_wml,node_x,node_y):

    file_0 = open(file_wml,'r')
    
    timestamp = -1
    node = 0
    node_counter = 0

    nodes_amount_t1 = 0
    
    aux_x = []
    aux_y = []
    
    for line in file_0:
        
        if line.startswith('\t\t\t<timestamp>'):
            # To skip the first time when no characters are read 
            if timestamp != -1:
                # We trust that the first timestamp will have all the nodes within the simulation area
                if timestamp == 0:
                    nodes_amount_t1 = max(len(aux_x),len(aux_y))
                                
                # Update the latest nodes if they are missing e.g. node 99 missing from 100 nodes
                if node_counter > nodes_amount_t1:
                    # TODO_1: Create a error file log to keep track of these errors with a thread that receives the errors and prints them
                    # TODO_2: Update backwards the first positions of the list when a bigger amount of nodes are detected
                    print 'Error parsing wml file: the timestamp 0 has not all the nodes within simulation area'

                while node_counter < nodes_amount_t1:
                    # The node is missing at this timestamp. We copy the values of the previous timestamp
                    # While loop in the case there are two or mode nodes missing consecutively
                    node = node_counter
                    node_counter += 1
                    
                    aux_x.insert(int(node), node_x[int(float(timestamp))-1][node])
                    aux_y.insert(int(node), node_y[int(float(timestamp))-1][node])
                
                # Insert in the matrix
                node_x.insert(timestamp, aux_x)
                node_y.insert(timestamp, aux_y)
                
                aux_x = []
                aux_y = []
                node_counter = 0
                
            i = 14
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                timestamp = int(float(line[14:i]))
            else:
                print 'Error: Bad parsing or .wml input file. EOF found and not the \'<\' character'
            
        elif line.startswith('\t\t\t<node id'):
            i = 13
            while line[i]!='\"' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                # We assume that the first timestamp has all the nodes displayed within the simulation area of BonnMotion
                while int(line[13:i]) != node_counter:
                    # The node is missing at this timestamp. We copy the values of the previous timestamp
                    # While loop in the case there are two or mode nodes missing consecutively
                    node = node_counter
                    node_counter += 1
                    
                    aux_x.insert(int(node), node_x[int(float(timestamp))-1][node])
                    aux_y.insert(int(node), node_y[int(float(timestamp))-1][node])
                
                # After inserting the missing node we have the current node and the node_counter updated    
                node = line[13:i]
                node_counter += 1
                
            else:
                print 'Error: Bad parsing or .wml input file. EOF found and not the \'\"\' character'
        elif line.startswith('\t\t\t\t\t<x'):
            i = 8
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                aux_x.insert(int(node), line[8:i])
            else:
                print 'Error: Bad parsing or .wml input file. EOF found and not the \'<\' character'
        elif line.startswith('\t\t\t\t\t<y'):
            i = 8
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                aux_y.insert(int(node), line[8:i])
            else:
                print 'Error: Bad parsing or .wml input file. EOF found and not the \'<\' character'
                         
        
    # This two lines are not commented to avoid have 301 elements in node_x and node_y as BonnMotion generates
    # for a simulation duration of e.g. 300 seconds, the timestamps from 0 up to 300 (included) 
    #node_x.insert(timestamp, aux_y)
    #node_y.insert(timestamp, aux_x)
    
    file_0.close()

    return nodes_amount_t1,int(float(timestamp))



def parser_wml_static(file_wml,node_x,node_y):
    """ Wml files parser for static scenarios i.e. there is no time variable
    
    Wml files parser for static scenarios i.e. there is no time variable. Thus, the scenario can be stored
    in a vector-like data structure, or a one-dimensional list (as we are using lists).
    
    """
    file_0 = open(file_wml,'r')
    
    timestamp = -1
    node = 0
    
    aux_x = []
    aux_y = []
    
    for line in file_0:
        
        if line.startswith('\t\t\t<timestamp>'):
            # To skip the first time when no characters are read.
            # After timestamp = 0 values are read, it enters here to include the values on the node_x and node_y lists
            if timestamp != -1:
                # We trust that the first timestamp will have all the nodes within the simulation area
                if timestamp == 0:
                    # Insert in the matrix
                    node_x.insert(timestamp, aux_x)
                    node_y.insert(timestamp, aux_y)
                
                # For the rest of empty timestamps, there are no values thus we merely skip them
                else:
                    # The break statement breaks out of the smallest enclosing for or while loop 
                    break
                    
            # Read timestamp value
            i = 14
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                timestamp = int(float(line[14:i]))
            else:
                print 'Error: Bad parsing or .wml input file. EOF found and not the \'<\' character'
            
        elif line.startswith('\t\t\t<node id'):
            i = 13
            while line[i]!='\"' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':    
                node = line[13:i]
                
            else:
                print 'Error: Bad parsing or .wml input file. EOF found and not the \'\"\' character'
        elif line.startswith('\t\t\t\t\t<x'):
            i = 8
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                aux_x.insert(int(node), line[8:i])
            else:
                print 'Error: Bad parsing or .wml input file. EOF found and not the \'<\' character'
        elif line.startswith('\t\t\t\t\t<y'):
            i = 8
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                aux_y.insert(int(node), line[8:i])
            else:
                print 'Error: Bad parsing or .wml input file. EOF found and not the \'<\' character'
                         
    
    file_0.close()


def parser_wml_boundaries(file_wml):
    """ Parse the .wml file and gets only the timestamps 0 and last """

    file_0 = open(file_wml,'r')
    
    node_x = []
    node_y = []
    
    timestamp = -1
    node = 0
    node_counter = 0

    nodes_amount_t1 = 0
    
    aux_x = []
    aux_y = []
    
    for line in file_0:
        
        if line.startswith('\t\t\t<timestamp>'):
            # To skip the first time when no characters are read 
            if timestamp != -1:
                # We trust that the first timestamp will have all the nodes within the simulation area
                if timestamp == 0:
                    nodes_amount_t1 = max(len(aux_x),len(aux_y))
                    
                    # Insert in the matrix only for the timestamp '0'
                    node_x.insert(timestamp, aux_x)
                    node_y.insert(timestamp, aux_y)
                                
                # Update the latest nodes if they are missing e.g. node 99 missing from 100 nodes
                if node_counter > nodes_amount_t1:
                    # TODO_1: Create a error file log to keep track of these errors 
                    # TODO_2: Update backwards the first positions of the list when a bigger amount of nodes are detected
                    logger.error('Error parsing wml file: the timestamp 0 has not all the nodes within simulation area')

                while node_counter < nodes_amount_t1:
                    # The node is missing at this timestamp. We copy the values of the previous timestamp
                    # While loop in the case there are two or mode nodes missing consecutively
                    node = node_counter
                    node_counter += 1
                    
                    aux_x.insert(int(node), node_x[int(float(timestamp))-1][node])
                    aux_y.insert(int(node), node_y[int(float(timestamp))-1][node])
                
                # the rest of the timestamps are not inserted in the list but the last one, which is inserted outside the for loop
                aux_x = []
                aux_y = []
                node_counter = 0
                
            i = 14
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                timestamp = int(float(line[14:i]))
            else:
                logger.error('Error: Bad parsing or .wml input file. EOF found and not the \'<\' character')
            
        elif line.startswith('\t\t\t<node id'):
            i = 13
            while line[i]!='\"' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                # We assume that the first timestamp has all the nodes displayed within the simulation area of BonnMotion
                while int(line[13:i]) != node_counter:
                    # The node is missing at this timestamp. We copy the values of the previous timestamp
                    # While loop in the case there are two or mode nodes missing consecutively
                    node = node_counter
                    node_counter += 1
                    
                    aux_x.insert(int(node), node_x[int(float(timestamp))-1][node])
                    aux_y.insert(int(node), node_y[int(float(timestamp))-1][node])
                
                # After inserting the missing node we have the current node and the node_counter updated    
                node = line[13:i]
                node_counter += 1
                
            else:
                logger.error('Error: Bad parsing or .wml input file. EOF found and not the \'\"\' character')
        elif line.startswith('\t\t\t\t\t<x'):
            i = 8
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                aux_x.insert(int(node), line[8:i])
            else:
                logger.error('Error: Bad parsing or .wml input file. EOF found and not the \'<\' character')
        elif line.startswith('\t\t\t\t\t<y'):
            i = 8
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                aux_y.insert(int(node), line[8:i])
            else:
                logger.error('Error: Bad parsing or .wml input file. EOF found and not the \'<\' character')
                         
    # insert the last timestamp information on the list 
    node_x.insert(timestamp, aux_x)
    node_y.insert(timestamp, aux_y)
    
    file_0.close()

    return node_x,node_y


