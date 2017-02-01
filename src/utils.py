#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 15:30:46 2017

@author: immersinn
"""

import os
from itertools import tee, starmap
from cytoolz.itertoolz import cons, pluck
import pickle
import xml.etree.ElementTree as ET
import socks
from sockshandler import SocksiPyHandler
from urllib import request

from textacy.corpus import Corpus


def get_main_dir():
    fd = os.path.split(os.path.realpath(os.path.split(__file__)[0]))[0]
    return(fd)


def get_data_dir():
    fd = get_main_dir()
    data_dir = os.path.join(fd, "data")
    return(data_dir)


def configure_tor_opener():
    opener = request.build_opener(SocksiPyHandler(socks.SOCKS5,
                                                  "127.0.0.1",
                                                  9050))
    return(opener)


def unzip(seq):
    """
    Borrowed from ``toolz.sandbox.core.unzip``, but using cytoolz instead of toolz
    to avoid the additional dependency.
    """
    seq = iter(seq)
    # check how many iterators we need
    try:
        first = tuple(next(seq))
    except StopIteration:
        return tuple()
    # and create them
    niters = len(first)
    seqs = tee(cons(first, seq), niters)
    return tuple(starmap(pluck, enumerate(seqs)))


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


def save_corpus(name, corpus, data_sub_dir="processed", compression='gzip'):
    path = os.path.join(get_data_dir(), data_sub_dir, name)
    os.mkdir(path)
    corpus.save(path=path, name=name, compression=compression)
    
    
def load_corpus(name, data_sub_dir="processed", compression='gzip'):
    path = os.path.join(get_data_dir(), data_sub_dir, name)
    return(Corpus.load(path=path, name=name, compression=compression))
        

def proc_doc_iterator(docs_iterator, tpp):
    def proc_item(entry):
        content = tpp(entry)
        return(content, entry.meta)
    return unzip((proc_item(item) for item in docs_iterator))


class doc_stream:
    
    def __init__(self, coll_name):
        self.coll_name = coll_name
        
        
    def __enter__(self):
        # Step 01: Create a MySQL connection to the table of file info
        # Step 02: Access "file_load" code to load files in MySQL list
        return(self)
    
    
    def __exit__(self,  exc_type, exc_value, traceback):
        pass
    
    
    def __next__(self,):
        # This should iterate over the file names and pull the doc,
        # mysql info
        pass
    
    