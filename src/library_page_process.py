#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 16:47:20 2017

@author: immersinn
"""

from bs4 import BeautifulSoup as bs


def extract_content_rows(soup):
    contents = soup.body.find_all('div', {'class' : "views-row"})
    return(contents)


def parse_content_row(content_element_soup):
    doc_page_match = ('h4', {'class' : "field-content"})
    doc_pdf_match =  ('tr', {'class' : "odd"})
    doc_pages_match = ('div', {'class' : "field-content"})
    
    doc_page_info = content_element_soup.find(doc_page_match[0], doc_page_match[1])
    doc_pdf_info = content_element_soup.find(doc_pdf_match[0], doc_pdf_match[1])
    doc_pages_info = content_element_soup.find(doc_pages_match[0], doc_pages_match[1])
    
    title = doc_page_info.text.strip()
    doc_page_url = doc_page_info.find('a')['href']
    doc_id = doc_page_url.split("/")[-1].strip()
    doc_pdf_url = doc_pdf_info.find('a')['href']
    pages = doc_pages_info.text.strip()
    return({"doc_id" : doc_id,
            "title" :title,
            "info_url" : doc_page_url, 
            "pdf_url" : doc_pdf_url,
            "n_pages" : pages})
    
    
def extract_docs_from_page(soup):
    contents = extract_content_rows(soup)
    info = [parse_content_row(c) for c in contents]
    return(info)
    
    
def docsFromLibraryPage(page):
    soup = bs(page, 'html.parser')
    doc_info = extract_docs_from_page(soup)
    return(doc_info)