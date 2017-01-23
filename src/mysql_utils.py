#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 17:29:21 2017

@author: immersinn
"""

import utils

import mysql.connector
from mysql.connector.cursor import MySQLCursor
from mysql.connector.errors import IntegrityError


DB = "cia"
TABLE = "pres_briefing_links"


def docinfo2MySQL(docs):
    """
    
    """
    u,p = utils.get_creds('MySQL')
    cnx = mysql.connector.connect(user=u, password=p, database=DB)
    cur = MySQLCursor(cnx)
    
    try:
        exists = lambda l: exists_base(cur, l)
        docs = [l for l in docs if not exists(l)]
        row_nbrs = dump_entries(cur, docs)
        cnx.commit()
        
    except IntegrityError:
        cnx.rollback()
        
    finally:
        cur.close()
        cnx.close()
        
    return(row_nbrs)


def docinfoFromMySQL():
    pass


def docinfoFromMySQLIter():
    """
    Return an iterator over the items in the MySQL db
    """
    pass


def dump_entries(cursor, entries):
    
    add_entry = ("INSERT INTO " + TABLE + " "
                 "(doc_id, title, info_url, pdf_url, n_pages) "
                 "VALUES (%(doc_id)s, %(title)s, %(info_url)s, %(pdf_url)s, %(n_pages)s)")
    
    rows = []
    dls = set()
    for entry in entries:
        if entry['doc_id'] not in dls:
            cursor.execute(add_entry, entry)
            rows.append(cursor.lastrowid)
            dls.update([entry['doc_id']])
        
    return(rows)


def exists_base(cursor, entry):
    sqlq = "SELECT (1) FROM " + TABLE + " WHERE doc_id = '{}' LIMIT 1"
    cursor.execute(sqlq.format(entry['doc_id']))
    if cursor.fetchone():
        return(True)
    else:
        return(False)