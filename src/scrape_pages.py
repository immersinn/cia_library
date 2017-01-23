#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 17:08:53 2017

@author: immersinn
"""

import time

import utils
from library_page_process import docsFromLibraryPage
from mysql_utils import docinfo2MySQL

lib_url_base = "https://www.cia.gov/library/readingroom/collection/presidents-daily-brief-1969-1977?page="


def main():
    
    rows = []
    for page_id in range(1,127):
        url = lib_url_base + str(page_id)
        page = utils.getPage(url, method='tor')
        info = docsFromLibraryPage(page)
        new_rows = docinfo2MySQL(info)
        rows.extend(new_rows)
        time.sleep(0.5)
        
    return(rows)


if __name__=="__main__":
    rows = main()
    print("Total documents found: {}".format(len(rows)))