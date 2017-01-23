#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 15:30:46 2017

@author: immersinn
"""

import os
import pickle
import requests

def getPage(url, method='req'):
    if method=='req':
        return(get_page_requests(url))
    elif method=='tor':
        pass


def get_page_requests(url):
    page = requests.get(url)
    return(page.content)

def pickle_data(file_name, data, folder="interim"):
    
    fd = os.path.abspath(os.path.join('..'))
    if folder=="raw" or folder=="r":
        data_path = os.path.join(fd, "data/raw")
    elif folder=="interim" or folder=="i":
        data_path = os.path.join(fd, "data/interim")
        
    file_name = file_name if file_name.endswith(".pkl") else file_name + ".pkl"
        
    with open(os.path.join(fd, data_path + file_name), 'wb') as f1:
        pickle.dump(data, f1)