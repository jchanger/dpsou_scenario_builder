""" This module contains functions for merging sub_scenarios .wml files into a single .wml file

"""

"""
Created on Feb 16, 2017

@author: J. Sanchez-Garcia
"""

import timing
import wml_files
import fill_missing

    
def write_positions(out_file,in_file,origin_x,origin_y):
    
    pos_text = in_file.readline()
    
    # create a new '<x>' line
    x_str = in_file.readline().strip('\t<x>/\n')
    x = float(x_str)+origin_x
    x_text = '\t\t\t\t\t<x>'+str(x)+'</x>\n'
    
    # create a new '<y>' line
    y_str = in_file.readline().strip('\t<y>/\n')
    y = float(y_str)+origin_y
    y_text = '\t\t\t\t\t<y>'+str(y)+'</y>\n'
    
    z_text = in_file.readline()
    
    pos_closing_text = in_file.readline()
    node_closing_text = in_file.readline()
    
    # write all the text into the out_file
    out_file.write(pos_text)
    out_file.write(x_text)
    out_file.write(y_text)
    out_file.write(z_text)
    out_file.write(pos_closing_text)
    out_file.write(node_closing_text)



def write_node_id(out_file,saved_line,node_offset):
    """ Writes the node id line from a sub_scenario file into the main .wml 
    """
    # Read node id
    node_id_str = saved_line.strip('\t<node id=">\n')
    
    if not node_id_str.isdigit():
        print 'Error: node id number from .wml file did not get a number'
    
    node_id = int(node_id_str)+node_offset
    
    node_id_text = '\t\t\t<node id="'+str(node_id)+'">\n'
    
    out_file.write(node_id_text)



def write_nodes(out_file,in_file,node_offset,prev_line,scen_j,origin_x,origin_y):
    """ writes all the nodes of a wml file starting from the current position of the file
    
    writes all the nodes of a wml file starting from the current position of the file.
    This function returns the number of nodes written for this timestamp from the 
    in_file.
    """
    
    wr_nodes = 0

  
    # when we read the other scenarios we need to read the first <timestamp> line
    # and discard it
    if scen_j != 0 and in_file.tell() == 0:
        in_file.readline()

    saved_line = in_file.readline()
    
    while  saved_line.startswith('\t\t\t<timestamp>') == False:
        # Write node id. Leaves the pointer at the beginning of '<positions>' line.
        # It works with the saved line as this has been already read in order to check
        # the end of timestamps with the saved_line variable
        write_node_id(out_file,saved_line,node_offset)
        
        # Writes 'x' and 'y' positions. Leave the reading pointer at the beginning of 
        # next '<node id...' line or '<timestamp>...' line
        write_positions(out_file,in_file,origin_x,origin_y)
        
        saved_line = in_file.readline()
        wr_nodes += 1
    
    if prev_line == None or scen_j == 0:
        # This case represents when a new timestamp is read from first sub_scenario
        return wr_nodes,saved_line
    else:
        # when the timestamp is read from other sub_scenarios different from the first one
        # the '<timestamp>' line from the first sub_scenario is maintained as the prev_line
        return wr_nodes,prev_line


def write_wml_timestamp(out_file,wml_timestamp):
    """ Writes the timestamp line into the out_file
    """
    out_file.write('\t\t\t<timestamp>'+str(wml_timestamp)+'.0</timestamp>\n')
    

    
def get_wml_timestamp(tstamp_line):
    
    # get the timestamp number before the '.'
    tstamp = tstamp_line.strip('\t<timestamp>/\n')[:-2]
         
    # check if the character is a number
    # NOTE: the 'isdigit()' function only works with positive numbers with no sign before the number
    # it doesn't work with decimals.
    if not tstamp.isdigit():
        print 'Error: reading timestamp number from .wml file did not get a number'
     
    return tstamp


def check_wml_timestamp(wml_file,prev_line,i,scen_j):
    """ Returns the .wml file timestamp number read from the current position
        
    Returns the .wml file timestamp number read from the current position. The 
    function reads till the end of line (the last \n character, leaving the reading
    pointer at the first character of the next line.
    """
    if prev_line == None:
        # This case occurs in the first timestamp i.e. the first line of a file
        new_line = wml_file.readline()
        
        wml_tstamp = get_wml_timestamp(new_line)
        wml_tstamp = int(wml_tstamp)
                
        if wml_tstamp != i:
            print 'Error: .wml timestamp does not coincide with the iteration'
    
    # In the case we read a new timestamp from the first sub_scenario
    elif scen_j == 0:
        wml_tstamp = get_wml_timestamp(prev_line)
        wml_tstamp = int(wml_tstamp)
                
        if wml_tstamp != i:
            print 'Error: .wml timestamp does not coincide with the iteration'
    
    # In this case we are reading a timestamp of a sub_scenario different from the 1st 
    else:
        wml_tstamp = i
    
    # TODO: Fix with a prev_line variable of type list
    # Trying to read a new line here from the sub_scenarios 2nd, 3rd... raises an error
    # bcs the timestamp line was already read also in the other sub_scenarios. For this 
    # reason the timestamp in this case is not checked here
    
    return wml_tstamp



def merge_sub_scenarios(bm_dir_name, duration, origins_list):
    """ Merge several sub_scenario .wml files into a single .wml file """
        
    # get timestamp for main .wml file
    timestamp = timing.timestamp_gen() 
      
    # create output file
    out_filename = bm_dir_name+timestamp+'_main.wml'
    out_file = open(out_filename, "w")
    
    # fill sub_scenarios missing nodes with their latest position
    # there is no need to order the sub_scenarios when filling the missing nodes 
    fill_missing.fill_missing_all_scenarios(bm_dir_name)
    
    # Open sub_scenario wml files
    wml_list = wml_files.open_sub_scenarios(bm_dir_name,'_fix.wml')
      
    # stores previous read lines for the transition from a timestamp to a new one in the wml file
    prev_line = None 
   
    # The first scenario is read as a for loop for each timestamp
    for i in range(0,duration):
        
        # for controlling the nodes id offset in several scenarios
        written_nodes = 0
    
        # whithin a timestamp we write all the nodes from all the sub_scenarios
        for scen_j in range(0,len(wml_list)):
            
            # check timestamp text for iteration 'i'
            wml_timestamp = check_wml_timestamp(wml_list[scen_j],prev_line,i,scen_j)
            
            if scen_j == 0:
                # write timestamp text for iteration 'i'
                write_wml_timestamp(out_file,wml_timestamp)
                        
            # write the sub_scenario nodes of first timestamp
            aux,prev_line = write_nodes(out_file,wml_list[scen_j],written_nodes,prev_line,scen_j,*origins_list[scen_j])
            
            written_nodes = written_nodes+aux
    
    
    # close all files
    out_file.close()
    wml_files.close_sub_scenarios(wml_list)


