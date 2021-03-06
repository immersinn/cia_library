#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 17:08:53 2017

@author: immersinn
"""

import os
import time
import logging

from bs4 import BeautifulSoup as bs
import requests

from utils import get_main_dir, configure_tor_opener
from mysql_utils import docinfo2MySQL


lib_url_base = "https://www.cia.gov/library/readingroom/collection/presidents-daily-brief-1969-1977?page="


def extract_content_rows(soup):
    contents = soup.body.find_all('div', {'class' : "views-row"})
    return(contents)


def parse_content_row(content_element_soup):
    doc_page_match = ('h4', {'class' : "field-content"})
#    doc_pdf_match =  ('tr', {'class' : "odd"})
    doc_pages_match = ('div', {'class' : "field-content"})
    
    doc_page_info = content_element_soup.find(doc_page_match[0], doc_page_match[1])
#    doc_pdf_info = content_element_soup.find(doc_pdf_match[0], doc_pdf_match[1])
    doc_pages_info = content_element_soup.find(doc_pages_match[0], doc_pages_match[1])
    
    title = doc_page_info.text.strip()
    doc_page_url = doc_page_info.find('a')['href']
    doc_id = doc_page_url.split("/")[-1].strip()
#    doc_pdf_url = doc_pdf_info.find('a')['href']
    pages = doc_pages_info.text.strip()
#    return({"doc_id" : doc_id,
#            "title" :title,
#            "info_url" : doc_page_url, 
#            "pdf_url" : doc_pdf_url,
#            "n_pages" : pages})
    
    return({"doc_id" : doc_id,
            "title" : title,
            "n_pages" : pages})

    
    
def extract_docs_from_page(soup):
    contents = extract_content_rows(soup)
    info = [parse_content_row(c) for c in contents]
    return(info)
    
    
def docsFromLibraryPage(page):
    soup = bs(page, 'html.parser')
    doc_info = extract_docs_from_page(soup)
    return(doc_info)


def get_page_contents(url, method='basic', opener=None):
    if method=='basic':
        return(get_page_contents_basic(url))
    elif method=="tor":
        return(get_page_contents_tor(url, opener))
        
        
def get_page_contents_basic(url):
    page = requests.get(url).content
    return(docsFromLibraryPage(page))
    
    
def get_page_contents_tor(url, opener):
    page = opener.open(url).read()
    return(docsFromLibraryPage(page))


def scrapeAndSave(sleep_time=1, method='basic', page_ids="all", verbose=False):
    
    if method=='tor':
        opener = configure_tor_opener()
        ip_addr = opener.open("http://icanhazip.com").read().strip()
        logging.info("IP Used: " + str(ip_addr))
        if verbose:
            print(ip_addr)
    else: 
        opener = None
        
    
    rows = []
    if page_ids == "all":
        page_ids = range(1,127)

    for page_id in page_ids:
        if page_id // 20 == 0:
            print("On page {}...".format(page_id))
        try:
            url = lib_url_base + str(page_id)
            info = get_page_contents(url, method=method, opener=opener)
            new_rows = docinfo2MySQL(info)
            rows.extend(new_rows)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except BaseException as err:
            err_type = str(type(err))
            err_msg = str(err.args)
            logging.error("Page " + str(page_id) + ": " + err_type + ': ' + err_msg)
            
        time.sleep(sleep_time)
        
    return(rows)
    
    
def main():
    # Configure logging
    fd = get_main_dir()
    logpath = os.path.join(fd, 'main_run.log')
    logging.basicConfig(filename=logpath,
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info("Starting scrape...")
    print("Retrieving contents...")
    rns = scrapeAndSave(sleep_time=.75, method='tor', page_ids="all")
    logging.info('Total new document pages added from pages: {}'.format(len(rns)))
    logging.info("Ending scrape...")
        
if __name__=="__main__":
    main()