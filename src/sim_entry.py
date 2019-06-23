#!/usr/bin/python

""" Launches a simple execution of create_n_scenarios application with specific parameters

--------------------------
Created on Oct 28, 2017

@author: J. Sanchez-Garcia
"""

import logging
from log_helpers import log_module
from launchers import launcher_one
from launchers import launcher_two

log_module.setup_logging()  
logger = logging.getLogger(__name__)

# Launcher flags
#---------------
# This creates an scenario locally
launch_local = 0

# This waits for a remote call to ask for generating an scenario 
launch_wait_sock = 1


# Launcher selection
# -------------------
if launch_local == 1:
    
    logger.info('Calling local launcher')
    # Calling launcher local
    launcher_one.launcher_local()
    
    
elif launch_wait_sock == 1:
    
    logger.info('Calling launcher remote')
    # Calling launcher remote
    launcher_two.launcher_remote()
    
    
