'''
Created on Oct 28, 2017

@author: J. Sanchez-Garcia
'''

import app_settings

DURATION = 90                   # DYNAMIC if called from auav. Movement of the victims duration
AREA_DIMENS = [5000,5000]       # DYNAMIC if called from auav. 
CLUSTERS_AMOUNT = 3             # DYNAMIC if called from auav. 

MAINTAIN_NODES=1                # Flag that makes the cluster share the nodes specified in the variable MAX_NODES_MAINTAINED
MAX_NODES_MAINTAINED=200

# folder for storing the simulation results, will be modified by 'launcher'
MAIN_OUTPUT_FOLDER =  app_settings.SCENARIO_PATH
OUTPUT_FOLDER = '' # DYNAMIC 

# timestamp of the scenario generation. It will be filled in each 'sim_core' call
TIMESTAMP = '' # DYNAMIC

# PARAMETERS GROUPING 
# -------------------

def update_CONFIG():
   
    # CONFIG is a dictionary to group parameters and ease the initial values passing to functions
    CONFIG = {'duration':DURATION,'area_dimens':AREA_DIMENS, 'clusters_amount':CLUSTERS_AMOUNT,\
              'maintain_nodes':MAINTAIN_NODES, 'max_nodes_maintained':MAX_NODES_MAINTAINED,\
              'main_output_folder':MAIN_OUTPUT_FOLDER, 'output_folder':OUTPUT_FOLDER, 'timestamp':TIMESTAMP}
    
    return CONFIG
