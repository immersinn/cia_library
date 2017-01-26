#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 17:30:32 2017

@author: immersinn
"""

import os
import time
import itertools
import logging

import requests
from utils import get_main_dir, configure_tor_opener, writePDF
from mysql_utils import docinfoFromMySQL
#from mongo_utils import docpdf2MDB


pdf_root_url = "https://www.cia.gov/library/readingroom/docs/"


def build_pdf_url(doc_id):
    return(pdf_root_url + "DOC_" + doc_id + '.pdf')


def get_pdf(url, method='tor', opener=None):
    if method=='basic':
        return(get_pdf_basic(url))
    elif method=="tor":
        return(get_pdf_tor(url, opener))
    
    
def get_pdf_basic(url):
    req = requests.get(url)
    pdf = req.content
    req.close()
    return(pdf)


def get_pdf_tor(url, opener):
    pdf = opener.open(url).read()
    return(pdf)


def scrapeAndSave(sleep_time=.2, limit=0, n_openers=4, method='tor', verbose=False):
    
    if method=='tor':
        logging.info("Creating {} Tor openers...".format(n_openers))
        openers = [configure_tor_opener() for _ in range(n_openers)]
        ip_addr = openers[0].open("http://icanhazip.com").read().strip()
        logging.info("IP Used: " + str(ip_addr))
        if verbose:
            print(ip_addr)
    else: 
        openers = [None]
    openers = itertools.cycle(openers)
        
    # Pull docs from MySQL
    docs = docinfoFromMySQL(limit=limit, fields=['doc_id'])
    logging.info("{} documents retrieved from mysql".format(len(docs)))
    
    rows = []
    for doc_ind, opener in zip(range(len(docs)), openers):    
        try:
            doc = docs[doc_ind]
            if doc_ind % 50 == 0:
                print("On document {}...".format(doc['doc_id']))
            pdf_url = build_pdf_url(doc['doc_id'])
            pdf = get_pdf(pdf_url, method=method, opener=opener)
            rows.append(writePDF(pdf, doc['doc_id']))
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except BaseException as err:
            err_type = str(type(err))
            err_msg = str(err.args)
            logging.error("Doc " + str(doc['doc_id']) + ": " + err_type + ': ' + err_msg)
            
        time.sleep(sleep_time)
        
    return(rows)


def main():
    # Configure logging
    fd = get_main_dir()
    logpath = os.path.join(fd, 'main_run_scrapepdfs.log')
    logging.basicConfig(filename=logpath,
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info("Starting scrape...")
    print("Retrieving PDFs...")
    rns = scrapeAndSave(sleep_time=.2, n_openers=8, method='tor', limit=0)
    logging.info('Total PDFs retrieved: {}'.format(len(rns)))
    logging.info("Ending scrape...")
        
        
if __name__=="__main__":
    main()