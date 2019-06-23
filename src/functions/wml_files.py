'''
Created on Feb 21, 2017

@author: J. Sanchez-Garcia
'''

import subprocess



def open_sub_scenarios(bm_dir_name,filetype):
    ''' Opens all sub_scenario files contained in the path provided as an argument
    '''
    
    # get the number of folders within the main scenario folder i.e. the number of sub_scenarios
    command = ['find',bm_dir_name, '-type', 'd']
    folders_list = subprocess.check_output(command)
    folders_list = folders_list.split('\n')
    folders_list.pop() 
    folders_list.pop(0)
    
    index_list = []
    first_char = len(bm_dir_name)
    
    # order the sub_scenarios folders_list according to the index of the folder name
    for folder in folders_list:
        index_list.append(int(folder[first_char+14:]))
    
    sorted_folders = [x for y,x in sorted(zip(index_list,folders_list))]
        
    # for loop for opening all sub_scenarios wml files (from its own folder location)
    wml_list = []
    for i in range(0,len(sorted_folders)):
        command = ['find',sorted_folders[i], '-name', '*'+filetype]
        wml_name = subprocess.check_output(command)
        wml_name = wml_name.strip('\n.')
        file_object = open(wml_name,'r')
        wml_list.append(file_object)
    
    return wml_list



def close_sub_scenarios(scen_list):
    ''' Closes all the sub_scenario .wml files opened
    '''
    
    for scen_file in scen_list:
        scen_file.close() 


def get_nodes_amount(wml_file):
    ''' Get the nodes amount of the sub_scenario from the .params file
    '''
    # opens the .params file 
    filename = wml_file.name[:-3]+'params'
    param_file = open(filename,'r')
    
    for read_line in param_file:
        if read_line.startswith('nn='):
            nodes_amount = int(read_line.strip('nn=\n'))
            break
        else:
            pass
    
    param_file.close()
    
    return nodes_amount
    
    
        