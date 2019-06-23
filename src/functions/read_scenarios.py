'''
Created on Jun 6, 2018

@author: J. Sanchez-Garcia
'''

import json
import unicodedata
import app_settings

def get_clusters(clusters_num):
    ''' get the scenarios parameters from a json file
    '''
    
    '''
    SCENARIO_NAME: the name of the scenario output file
    SIZE: the scenario size in the form [x_max dimension,y_max dimension]
    DURATION: the time duration of the simulation
    
    SUB_SCENARIO_1: a list with the name of the subscenario 1 and its features
        - SUB_SCENARIO_1[0]: sub_scenario_1 name
        - SUB_SCENARIO_1[1]: sub_scenario_1 'x' origin (it must be within the SIZE of the final scenario)
        - SUB_SCENARIO_1[2]: sub_scenario_1 'y' origin (it must be within the SIZE of the final scenario)
        - SUB_SCENARIO_1[3]: sub_scenario_1 'x' dimension (it must be within the SIZE of the final scenario)
        - SUB_SCENARIO_1[4]: sub_scenario_1 'y' dimension (it must be within the SIZE of the final scenario)s
        - SUB_SCENARIO_1[5]: sub_scenario_1 number of nodes
        - SUB_SCENARIO_1[6]: sub_scenario_1 BM mobility model
        - SUB_SCENARIO_1[7]: sub_scenario_1 other features, for mobility models which need more, 
        e.g. skipped seconds
        
    SUB_SCENARIO_2: a list with the name of the subscenario 2 and its features
        - Similar to SUB_SCENARIO_1
'''
    
    # Just as a note, old scenarios were defined like is shown below
#     SUB_SCENARIO_1 = ('subscen_1',500,4000,100,'RandomWaypoint',3600,DURATION)
#     ORIGIN_S_SUB_1 = (200,200)
#     SUB_SCENARIO_2 = ('subscen_2',500,500,60,'RandomWaypoint',3600,DURATION)
#     ORIGIN_S_SUB_2 = (3000,200)
#     SUB_SCENARIO_3 = ('subscen_3',500,1000,40,'RandomWaypoint',3600,DURATION)
#     ORIGIN_S_SUB_3 = (2500,2500)

        
    """ The sub_scenarios defined above will compose a final scenario similar to the one shown below
       (although these are not depicted in a accurate scale)
    
     ---------------------------
     |            ____         |
     |           |    |        |
     | --------  |_3__|        |
     | |      |                |
     | |      |                |
     | |   1  |     -------    |
     | |      |     |     |    |
     | |      |     |  2  |    |
     | --------     -------    |
     ---------------------------
    
    """
    
    file_path = app_settings.SCEN_BUILDER_PATH+'/src/clusters.json'
    
    scen_list = []
    origins_list = []
    
    with open(file_path, 'r') as f:
        json_data = json.load(f)
    
    #read json file
    for i in range(clusters_num):
        cluster_aux = []
        origins_aux = []
        
        cluster_aux.append(unicodedata.normalize('NFKD', json_data["clusters"][i]["name"]).encode('ascii','ignore'))
        cluster_aux.append(float(json_data["clusters"][i]["x_width"]))
        cluster_aux.append(float(json_data["clusters"][i]["y_width"]))
        cluster_aux.append(int(json_data["clusters"][i]["nodes"]))
        cluster_aux.append(unicodedata.normalize('NFKD', json_data["clusters"][i]["model"]).encode('ascii','ignore'))
        cluster_aux.append(int(json_data["clusters"][i]["initial_offset"]))

        
        origins_aux.append(float(json_data["clusters"][i]["x_origin"]))
        origins_aux.append(float(json_data["clusters"][i]["y_origin"]))

        scen_list.append(cluster_aux)
        origins_list.append(origins_aux)
        
        del cluster_aux
        del origins_aux
        
    return scen_list,origins_list


def redistribute_cluster_nodes(scenario_list, CONFIG):
    ''' redistribute the maximum number of nodes among the clusters
    '''
    
    max_nodes = CONFIG["max_nodes_maintained"]
    clusters = CONFIG["clusters_amount"]
    
    assigned_nodes = 0
    
    for i in range(clusters):
        
        if i != clusters-1:
            # assign half of the nodes available to the next cluster
            scenario_list[i][3] = (max_nodes-assigned_nodes)/2 
            assigned_nodes = assigned_nodes + (max_nodes-assigned_nodes)/2
        else:            
            # assign the rest of the nodes to the last cluster
            scenario_list[i][3]=max_nodes-assigned_nodes

        
