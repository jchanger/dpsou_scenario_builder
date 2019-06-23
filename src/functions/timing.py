'''
Created on Jul 31, 2015

@author: J. Sanchez-Garcia
'''

import time
import datetime


def timestamp_gen():
    """ Function for generating an specific timestamp for the output files extension
    """
    ts = time.time()
    
    t_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d-%H%M%S')
    t_stamp = t_stamp[2:] # slices the string removing the '20' from the year
    
    return t_stamp
