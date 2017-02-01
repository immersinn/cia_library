#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 13:11:21 2017

@author: immersinn
"""

import warnings


target_page_break = "Declassified in Part - Sanitized Copy Approved for Release 2016/"


def flag_declass_year(token):
    if token.startswith('2018') or \
       token.startswith('2016') or \
       token.startswith('2015'):
        return True
    else:
        return False
    
    
def flag_declass_statement(token):
    if token.startswith('Dec'):
        return(True)
    else:
        return(False)
    

def decode_doc(doc):
    return(doc.decode('utf8', 'replace'))
    
    
def tokenize_doc(doc, method='simple'):
    return(doc.split())
    
    
def split_into_pages(tokens, n_pages):
    declass_year_positions = [flag_declass_year(token) for token in tokens]
    
    if sum(declass_year_positions) % 2 == 0:
        pages = []
        counter = 0
            
        # Iterate tokens:
        # First, find the first year "hit" to start recording
        # Subsequently, look for pairs of years to inform when to
        # switch between "record" and "burn" states
        state = None
        while counter < len(tokens):
            if not state:
                if declass_year_positions[counter]:
                    state = 'record'
                    page = []
            else:
                if declass_year_positions[counter]:
                    if state == 'record':
                        pages.append(page)
                        state = 'burn'
                    elif state == 'burn':
                        page = []
                        state = 'record'
                else:
                    if state == 'record':
                        page.append(tokens[counter])
                    elif state == 'burn':
                        pass
            counter += 1
        if len(pages) != n_pages:
            warnings.warn("Number of pages found does not match expected number of pages",
                          UserWarning)
        return(pages)
            
    else:
        err_msg = "uneven number of year flags found"
        raise AttributeError(err_msg)
    
    
def trim_and_filter_pages(pages):
    pages = [trim_and_filter_page(page) for page in pages]
    pages = [page for page in pages if page]
    return(pages)


def trim_and_filter_page(page):
    """
    Use the "FOR THE PRESIDENT ONLY" tags and the start, end of each
    page to further trim the pages that have text.
    
    Not all pages (e.g., "Title Page" and Maps) have these lines,
    so cannot use to split pages.  But, because it is missing from 
    these page types, we can use it to filter out pages.
    
    THIS METHOD IS NOT RELIABLE; SOME TEXT PAGES HAVE THIS TAG COVERED UP
    """
    pres_seq = "FOR THE PRESIDENT ONLY"
    page = ' '.join(page)
    pos = page.find(pres_seq)
    if pos > -1 and pos < 100:
        page = page[(pos + len(pres_seq)):]
        pos = page.find(pres_seq)
        page = page[:pos]
        return(page)
    else:
        return(page)
    

def new_page_split(tokens, n_pages):
    
    declass_state_positions = [flag_declass_statement(token) for token in tokens]
    declass_year_positions = [flag_declass_year(token) for token in tokens]
    declass_positions = [dp or yp for dp, yp in zip(declass_state_positions,
                                                    declass_year_positions)]
    
    pages = []
    counter = 0
    record = False
    while counter < len(tokens):
        if not record:
            if declass_year_positions[counter]:
                temp = declass_positions[(counter + 1) : (counter + 12)]
                for i,t in enumerate(temp):
                    if t:
                        counter += i + 1
                record = True
                page = []
        else:
            if declass_year_positions[counter]:
                pages.append(page)
                page = []
                
                temp = declass_positions[(counter + 1) : (counter + 25)]
                placeholder = -1
                updates = 0
                for i,t in enumerate(temp):
                    if t and updates < 4:
                        placeholder = i
                        updates += 1
                counter += placeholder + 1
            else:
                page.append(tokens[counter])
        counter += 1
    
    if len(pages) != n_pages:
        warnings.warn("Number of pages found does not match expected number of pages",
                      UserWarning)
        
    return(pages)
                
        
def processDoc(doc_dict):
    
    doc = doc_dict['text']
    n_pages = doc_dict['n_pages']
    
    tokens = tokenize_doc(decode_doc(doc))
#    pages = split_into_pages(tokens, n_pages)
    pages = new_page_split(tokens, n_pages)
    pages = trim_and_filter_pages(pages)
    doc_dict['pages'] = pages
    return(doc_dict)

