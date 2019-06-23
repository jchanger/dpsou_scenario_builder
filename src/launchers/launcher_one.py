#!/usr/bin/python

""" Launches a simple execution of create_n_scenarios application with specific parameters

--------------------------
Created on May 11, 2017

@author: J. Sanchez-Garcia
"""

import logging
import create_n_scenarios
import settings

def launcher_local():
    
    logger = logging.getLogger(__name__)
    
    # Simple sim_entry of the scenario_builder application
    DURATION = settings.DURATION
    
    logger.info('Calling to generate local scenario with duration: '+str(DURATION))
    create_n_scenarios.generate_scenarios(DURATION)