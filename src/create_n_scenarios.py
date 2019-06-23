#!/usr/bin/python

"""This module creates BonnMotion scenarios of different characteristics

This module creates BonnMotion scenarios of different characteristics, specifically:
   - It creates 2 scenarios launching BonnMotion
   - Converts the scenarios with WiseML
   - Merges the two scenarios in 1 '.wml' file according to a defined displacement of the subscenarios
   (which are specified by the user)
   - Copy the files to the scenario_builder tool path (this module tool), specifically within the 'built_scenarios'
   
Note that these variables are defined in the 'app_settings module':
   - BonnMotion is installed in the path:  
        BM_PATH = '/home/jesus/workspace_bonn/bonnmotion-2.1.3/'
   - The scenario_builder tool (this module tool) is installed in the path:
        SCENARIO_PATH = '/home/jesus/e_workspace/scenario_builder/src/built_scenarios'
    
"""

'''
Created on Feb 2, 2017

@author: J. Sanchez-Garcia
'''


import subprocess
import app_settings
import settings
from subprocess import PIPE, Popen
from create_scenario import create_sub_scenario
from functions import timing
from functions import merge_scenarios
from functions import read_scenarios
from functions import plotting


def generate_scenarios(CONFIG):
    """ generate the scenario wml file with all the clusters 
    """

    CONFIG = settings.update_CONFIG()
    duration = CONFIG["duration"]
    clusters_amount = CONFIG["clusters_amount"]
    
    # Table for reading the scenarios in an ordered manner
    scen_list,ORIGINS = read_scenarios.get_clusters(clusters_amount)
    
    if CONFIG['maintain_nodes'] == 1:
        read_scenarios.redistribute_cluster_nodes(scen_list,CONFIG)
        
    
    #-----------------------------------------------------------------------------
    # Main procedure
    #-----------------------------------------------------------------------------
    
    # Generates timestamp for adding to the filename
    settings.TIMESTAMP = timing.timestamp_gen() # modifies only local CONFIG
    CONFIG = settings.update_CONFIG()

    # the main scenario directory is created in the BM workspace, it will contain sub_scenario folders
    bm_dir_name = app_settings.BM_PATH+'bin/built_scenarios/'+str(CONFIG['timestamp'])+'/'
    command = ['mkdir', bm_dir_name]
    subprocess.call(command)
    
    # update config with timestamp and files paths
    settings.OUTPUT_FOLDER = bm_dir_name
    CONFIG = settings.update_CONFIG()

    
    for index,scen_i in enumerate(scen_list):
        if index == 0:
            print ""
            
        print "Generating cluster "+str(index)
        create_sub_scenario(bm_dir_name,index,duration,ORIGINS[index],*scen_i)
    
    # parse files to join several sub-scenarios
    print '\nMerging clusters into the scenario...'
    merge_scenarios.merge_sub_scenarios(bm_dir_name,duration,ORIGINS)
    
    # generate a general 'params' file for the merged scenario
    command = ['find',bm_dir_name,'-name','*.params']
    popen_proc = Popen(command,stdout=PIPE)
    params_filenames = popen_proc.stdout.read()
    params_filenames = params_filenames.split('\n')
    del params_filenames[-1] # remove the last empty string
    params_filenames.sort()
    
    general_param_file = open(bm_dir_name+str(CONFIG['timestamp'])+'.params','w')
    
    for filename_i in params_filenames:
        file_i = open(filename_i,'r')
        
        for line in file_i:
            general_param_file.write(line)
        
        general_param_file.write('\n\n')
        file_i.close()
    
    general_param_file.close()
    
    # Copy files to python workspace
    command = ['mv',bm_dir_name,app_settings.SCENARIO_PATH]
    subprocess.call(command)
    
    # returns the path of the output folder
    out_folder_path = app_settings.SCENARIO_PATH+'/'+str(CONFIG['timestamp'])
    
    # organize return information
    clusters=[]
    nodes_amount = 0
    
    for i,scen_i in enumerate(scen_list):
        aux_origin = [ORIGINS[i][0],ORIGINS[i][1]]
        aux_dimension=[scen_i[1],scen_i[2]]
        cluster_i=[aux_origin,aux_dimension]
        clusters.append(cluster_i)
        
        nodes_amount = nodes_amount + scen_i[3]
    
        
    # plot scenario figure
    print "Plotting scenario..."
    plotting.create_scenario_figure(CONFIG['timestamp'], CONFIG)
    
    print 'Scenario generation finished'

    return out_folder_path,clusters,nodes_amount
    
if __name__ == "__main__":
    generate_scenarios()
    
    