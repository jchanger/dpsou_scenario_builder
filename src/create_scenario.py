#!/usr/bin/python

"""This module creates BonnMotion scenarios of different characteristics as a sub_scenario

This module creates BonnMotion scenarios of different characteristics, specifically:
   - It creates 1 scenario launching BonnMotion
   - Converts the scenario with WiseML
      
Note that:
   - BonnMotion is installed in the path:  
        BM_PATH = '/home/jesus/workspace_bonn/bonnmotion-2.1.3/'
   - The scenario_builder tool (this module tool) is installed in the path:
        SCENARIO_PATH = '/home/jesus/e_workspace/scenario_builder/src/built_scenarios'
    
"""

'''
Created on Feb 1, 2017

@author: J. Sanchez-Garcia
'''

import os
import subprocess
import app_settings

from functions import timing

def create_sub_scenario(bm_dir_name,index,duration,origin,scenario_name,x_dim,y_dim,nodes_amount,bm_model,skip_secs):
    '''
        INDEX: a number indicating the scenario index related to the set of sub_scenarios
        SCENARIO_NAME: the name for the output file
        SIZE: the scenario size in the form [x_max dimension,y_max dimension]
        NODES_AMOUNT: the number of nodes
        DURATION: the time duration of the simulation
    '''
    
    timestamp = timing.timestamp_gen()
    
    sub_bm_dir_name = bm_dir_name+str(timestamp)+'_'+str(index)+'/'
    command = ['mkdir', sub_bm_dir_name]
    subprocess.call(command)
        
    # Call to BonnMotion
    command = [app_settings.BM_PATH+'bin/bm','-f',sub_bm_dir_name+scenario_name,bm_model, \
               '-n',str(nodes_amount),'-x', str(x_dim), '-y', str(y_dim), '-d', str(duration),'-i', str(skip_secs)]
    stdout_null = open(os.devnull,'w')
    subprocess.call(command,stdout=stdout_null)
    
    # Save the bm command in a textfile for remembering it
    bm_command = ' '.join(command) # converts the list into a string separating elements by a space
    
    # Execute WiseML
    command = [app_settings.BM_PATH+'bin/bm', 'WiseML','-f',sub_bm_dir_name+scenario_name, \
               '-L', str(1.0)]
    subprocess.call(command,stdout=stdout_null)

    # Add command to the 'param' file that BM (wiseML) creates automatically
    param_filename = sub_bm_dir_name+scenario_name+'.params'
    param_file = open(param_filename,'r+')
    
    prev_text=[]
    
    for line in param_file:
        prev_text.append(line)
    
    param_file.seek(0)
    
    param_file.write(scenario_name+': Scenario_'+timestamp+'\n')
    param_file.write('---------------------------------\n')
    
    param_file.write('\nGeneration command:\n')
    param_file.write(bm_command+'\n')
    
    # Add the origin and dimension information to the param file
    param_file.write('\nCluster information:\n')
    param_file.write('origin (x,y): '+str(origin)+'\n')
    param_file.write('dimension (max_x,max_y): '+str((x_dim,y_dim))+'\n')
    
    param_file.write('\nParameters:\n')
    for item in prev_text:
        param_file.write(item)
    
    param_file.write('\n##################################################################################\n')
    
    param_file.close()
    
    
    
    