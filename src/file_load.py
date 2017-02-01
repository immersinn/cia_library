#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 12:31:04 2017

@author: immersinn
"""

import os

import mysql_utils


data_dir = '/home/immersinn/gits/cia_library/data/interim/presidents-daily-brief-1969-1977_dats/'


def fibseq(max_val):
    a, b = 1, 2
    while a < max_val:
        yield a
        a, b = b, a + b
        
        
def retrieve_docs(collection="presidents-daily-brief-1969-1977", which="all"):
    
    if which == "all":
        file_names = os.listdir(data_dir)
        
    docs = []
    for fn in file_names:
        with open(os.path.join(data_dir, fn), 'rb') as f:
            docs.append({"doc_id" : fn.strip('.bin').strip('DOC_'),
                         "raw" : f.read()
                         })
    
    # Merge data from MySQL
    doc_names = [dn.strip('.bin').strip('DOC_') for dn in file_names]
    doc_info = doc_info_mysql(doc_names)
    for doc in docs:
        try:
            entry = [di for di in doc_info if di['doc_id'] == doc['doc_id']][0]
            doc['n_pages'] = entry['n_pages']
            doc['title'] = entry['title']
        except IndexError:
            print(doc['doc_id'])
        
    return(docs)


def doc_info_mysql(doc_names):
    doc_info = mysql_utils.docinfoFromMySQL(fields = "all",
                                            which = doc_names)
    return(doc_info)


def main():
    files = os.listdir(data_dir)
    keep = [k for k in fibseq(len(files))]
    docs = retrieve_docs(which=[files[k] for k in keep])
    return(docs)