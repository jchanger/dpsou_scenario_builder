'''
Created on Feb 2, 2017

@author: J. Sanchez-Garcia
'''

""" This module allows to create global values that can be accessed from different modules

These variables are:
- BonnMotion is installed in the path:
BM_PATH = '/home/jesus/workspace_bonn/bonnmotion-2.1.3/'
- The scenario_builder tool (this module tool) is installed in the path:
SCENARIO_PATH = '/home/jesus/e_workspace/scenario_builder/src/built_scenarios'
NOTE: depending on the way the repositories have been connected to eclipse (selecting
either the option "local" or "URL" the SCENARIO_PATH may change from the local repository
path or the workspace path.
"""


MAIN_APP_PATH='/home/jesus/Develop/uav_ns'
BM_PATH = str(MAIN_APP_PATH)+'/bonnmotion/bonnmotion-3.0.1/'
SCEN_BUILDER_PATH =  str(MAIN_APP_PATH)+'/scenario_builder'
SCENARIO_PATH =  str(MAIN_APP_PATH)+'/scenario_builder/src/built_scenarios'
