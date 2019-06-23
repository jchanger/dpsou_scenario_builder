'''
Created on Feb 21, 2017

@author: J. Sanchez-Garcia
'''

import wml_files


def write_missing_node(out_file,node_counter,old_x,old_y):
    
    
    # create the missing node text line
    node_text = '\t\t\t<node id="'+str(node_counter)+'">\n'
    out_file.write(node_text) 
    
    # write <position> line into out_file
    pos_text = '\t\t\t\t<position>\n'
    out_file.write(pos_text) 
    
    # read node counter last 'x' position
    x_text = '\t\t\t\t\t<x>'+str(old_x)+'</x>\n'
    out_file.write(x_text)
    
    # read node counter last 'y' position
    y_text = '\t\t\t\t\t<y>'+str(old_y)+'</y>\n'
    out_file.write(y_text)
    
    # write 'z' line
    z_text = '\t\t\t\t\t<z>0.0</z>\n'
    out_file.write(z_text)
    
    # write </position>
    end_pos_text = '\t\t\t\t</position>\n'
    out_file.write(end_pos_text)
    
    # write </node>
    end_node_text = '\t\t\t</node>\n'
    out_file.write(end_node_text)
                    
                    

def fill_missing_nodes(in_file,nodes_amount):
    '''Traverses a scenario .wml file, filling the missing nodes in each timestamps with their latest positions
    '''
        
    # Open out file in the correct folder
    out_filename = in_file.name[:-4]+'_fix.wml'
    out_file = open(out_filename, "w")
    
    # node list is a list of coordinates in the form [x,y]
    node_list=[]
    for j in range(0,int(nodes_amount)):
        node_list.append([0.0,0.0])
    
    # variable for counting actual nodes within a timestamp
    node_counter = 0
    start = 1
    
    file_line = in_file.readline()
    
    # read() and readline() returns the empty string when the EOF is reached
    # However there is not a specific EOF character
    while file_line != '':
        if file_line.startswith('\t\t\t<timestamp>'):
            if node_counter == nodes_amount:
                
                node_counter = 0 
                
                # the <timestamp> line is directly copied into the out_file
                out_file.write(file_line)
                
                # read next line
                file_line = in_file.readline()
            
            # this case is when the missing node is the last one of the timestamp
            elif start == 1:
                # the <timestamp> line is directly copied into the out_file
                out_file.write(file_line)
                
                # read next line
                file_line = in_file.readline()
                
                start = 0
                
            else:

                write_missing_node(out_file,node_counter,*node_list[node_counter])
                
                node_counter += 1
                
        else:
            if file_line.startswith('\t\t\t<node id'):
                # get the node id
                node_id = file_line.strip('\t<node id=">\n')
                node_id = int(node_id)
                
                if node_id == node_counter:
                    # write node_id line into out_file
                    out_file.write(file_line)
                    
                    # write <position> line into out_file
                    file_line = in_file.readline()
                    out_file.write(file_line)
                    
                    # get x position and write into the out_file
                    file_line = in_file.readline()
                    x = file_line.strip('\t<x>/\n')
                    out_file.write(file_line)
                    
                    # get y position and write into the out_file
                    file_line = in_file.readline()
                    y = file_line.strip('\t<y>/\n')
                    out_file.write(file_line)
                    
                    # get z position and write into the out_file
                    file_line = in_file.readline()
                    out_file.write(file_line)
                    
                    # get </position> and write into the out_file
                    file_line = in_file.readline()
                    out_file.write(file_line)
                    
                    # get </node> and write into the out_file
                    file_line = in_file.readline()
                    out_file.write(file_line)

                    # save x,y in node_list as the latest valid values
                    node_list[node_counter][0]=x
                    node_list[node_counter][1]=y
                                        
                    node_counter += 1
                    file_line = in_file.readline()
                
                else:           
                    write_missing_node(out_file,node_counter,node_list[node_counter][0],node_list[node_counter][1])
                    
                    node_counter += 1
                    
                    # a new line is not read because it was read for a higher node id already
                    
    # close out_file
    out_file.close()
        
        

def fill_missing_all_scenarios(bm_dir_name):
    ''' Traverses all scenario .wml files contained in the provided folder path, filling the missing nodes in each of them
    '''
    
    # Open sub_scenario wml files
    wml_list = wml_files.open_sub_scenarios(bm_dir_name,'.wml')
    
    for wml_file in wml_list:
        nodes_amount = wml_files.get_nodes_amount(wml_file)   
        fill_missing_nodes(wml_file,nodes_amount)
    
    wml_files.close_sub_scenarios(wml_list)
    
    