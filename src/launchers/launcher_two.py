#!/usr/bin/python

""" Launches a simple execution of create_n_scenarios application with specific parameters

--------------------------
Created on May 11, 2017

@author: J. Sanchez-Garcia
"""

import logging
import server_socket

def launcher_remote():

    logger = logging.getLogger(__name__)

    # Turns the server up for listening for scenario generation requests
    logger.info('Setting up listen_requests socket for receiving scenario generation queries')
    server_socket.listen_requests()