#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 17:30:32 2017

@author: immersinn
"""

import time
from utils import getPDFFromURL, savePDF
from mysql_utils import docinfoFromMySQLIter


def main():
    print('Scraping PDF files...')
    doc_iter = docinfoFromMySQLIter()
    for i,info in enumerate(doc_iter):
        if i // 100 == 0:
            print('  Retrieving PDF for doc {} ({})...'.format(info['doc_id'], i))
        pdf = getPDFFromURL(info['pdf_url'])
        status = savePDF(info['doc_id'], pdf)
        if status == 'Pass':
            pass
        time.sleep(0.5)
        