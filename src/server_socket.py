#!/usr/bin/python

""" This module launches the scenario_builder as a server, listening for client requests to generate new scenarios (the auav simulator)

Created on May 9, 2017

@author: root
"""


import socket
import time
import create_n_scenarios
import json
import settings
import unicodedata
from _socket import SHUT_RDWR

HOST = 'localhost' # 127.0.0.1 can be also used
PORT = 10000
BUFFER_SIZE = 1024

def listen_requests():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the server to the port
    server_address = ('localhost', 10000)   # This follows the syntax (host, port) 
    print 'starting up on %s port %s' % server_address
    sock.bind(server_address)
    
    # Listen for incoming connections
    sock.listen(1)
    
    # Wait for a connection
    print 'waiting for a connection'
    
    connection, client_address = sock.accept()  
    print 'connection from', client_address
    
    # Receive the data 
    while True:
        data_size = connection.recv(BUFFER_SIZE)
        
        if data_size:
            break
        
    connection.sendall('ACK')
    
    data = connection.recv(int(data_size))
    print 'received %s ' % data
    
    json_parsed = json.loads(data)
    duration = int(json_parsed["duration"])    
    clusters_amount = int(json_parsed['clusters_amount'])
    area_dimens = [int(json_parsed["area_dimens"][0]),int(json_parsed["area_dimens"][1])] 
    
    
    # call to generate scenario
    settings.DURATION = duration
    settings.AREA_DIMENS = area_dimens
    settings.CLUSTERS_AMOUNT = clusters_amount 
    CONFIG = settings.update_CONFIG()
    
    folder_path,clusters,nodes_amount = create_n_scenarios.generate_scenarios(CONFIG)
    
    # generate json-like object
    js_obj = {"scenario":folder_path,"clusters":clusters,"nodes_amount":nodes_amount}
    message = json.dumps(js_obj)
    
    data_size = len(message)
    
    connection.sendall(str(data_size))
    
    time.sleep(10)
    
    connection.sendall(message)
    
    # Clean up the connection
    print 'Closing server connection'
    connection.shutdown(SHUT_RDWR)
    connection.close()
        
        
        