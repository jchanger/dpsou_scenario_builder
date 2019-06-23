'''
Created on 8 Jun 2018

@author: jesus
'''

import matplotlib   
matplotlib.use('Agg')   # for running the script on the server without graphics system up

import matplotlib.pylab as plt
from functions import parsers
import settings
from subprocess import PIPE, Popen


def plot_scenario(nodes_xpos,nodes_ypos,CONFIG,scenario_output_folder):
    """ Plots a snapshot of the scenario at timestamps 0 and the last """
    
    fig = plt.figure()
    
    # timestamp 0
    ax = fig.add_subplot(121)
    
    ax.plot(nodes_xpos[0],nodes_ypos[0],linestyle='None',marker='.',color='green')
    
    ax.set_xlabel("x coordinate (m)")
    ax.set_ylabel("y coordinate (m)")
    ax.set_title("Nodes map at time=0")
    x_dimension = CONFIG['area_dimens'][0]
    y_dimension = CONFIG['area_dimens'][1]
    ax.set_xlim([0,x_dimension])
    ax.set_ylim([0,y_dimension])
    ax.set_aspect('equal')
    
    # last timestamp
    ax = fig.add_subplot(122)
    
    ax.plot(nodes_xpos[1],nodes_ypos[1],linestyle='None',marker='.',color='green')
    
    ax.set_xlabel("x coordinate (m)")
#     #ax.set_ylabel("y coordinate (m)") # y_label is equal for both subplots
    ax.set_title("Nodes map at last time="+str(CONFIG['duration']))
    x_dimension = CONFIG['area_dimens'][0]
    y_dimension = CONFIG['area_dimens'][1]
    ax.set_xlim([0,x_dimension])
    ax.set_ylim([0,y_dimension])
    ax.set_aspect('equal')
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(scenario_output_folder+'/'+CONFIG['timestamp']+'_nodes_map.svg',format='svg',dpi=600,bbox_inches='tight')
    plt.close('all')
    
    
    
# Called from another module
def create_scenario_figure(scenario_folder, CONFIG):
    
    scenario_path = CONFIG['main_output_folder']+'/'+scenario_folder
    
    # generate a general 'params' file for the merged scenario
    command = ['find',scenario_path,'-name','*_main.wml']
    popen_proc = Popen(command,stdout=PIPE)
    params_filenames = popen_proc.stdout.read()
    params_filenames = params_filenames.split('\n')
    del params_filenames[-1] # remove the last empty string
    
    input_file = params_filenames[0]
    
    nodes_xpos,nodes_ypos = parsers.parser_wml_boundaries(input_file)
    plot_scenario(nodes_xpos,nodes_ypos,CONFIG, scenario_path) 
