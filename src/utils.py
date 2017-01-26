#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 15:30:46 2017

@author: immersinn
"""

import os
import pickle
import xml.etree.ElementTree as ET
import socks
from sockshandler import SocksiPyHandler
from urllib import request


def get_main_dir():
    fd = os.path.split(os.path.realpath(os.path.split(__file__)[0]))[0]
    return(fd)


def configure_tor_opener():
    opener = request.build_opener(SocksiPyHandler(socks.SOCKS5,
                                                  "127.0.0.1",
                                                  9050))
    return(opener)


def pickle_data(file_name, data, folder="interim"):
    
    fd = os.path.abspath(os.path.join('..'))
    if folder=="raw" or folder=="r":
        data_path = os.path.join(fd, "data/raw")
    elif folder=="interim" or folder=="i":
        data_path = os.path.join(fd, "data/interim")
        
    file_name = file_name if file_name.endswith(".pkl") else file_name + ".pkl"
        
    with open(os.path.join(fd, data_path + file_name), 'wb') as f1:
        pickle.dump(data, f1)
        
        
def get_creds(name):
    fd = get_main_dir()
    cred_path = os.path.join(fd, 'credentials.creds')
    tree = ET.parse(cred_path)
    root = tree.getroot()
    
    keep = ET.Element('')
    username = ''
    password = ''
    
    for elem in root:
        if elem.attrib['name'] == name:
            keep = elem
    if keep.tag:
        username = keep.find('username').text
        password = keep.find('password').text
        
    return(username, password)


def writePDF(pdf_bytes, doc_id):
    fd = os.path.abspath(os.path.join('..'))
    data_path = os.path.join(fd, "data/raw/presidents-daily-brief-1969-1977_pdfs")
    with open(os.path.join(data_path, "DOC_" + doc_id + ".pdf"), 'wb') as f1:
        f1.write(pdf_bytes)
    return(1)
        