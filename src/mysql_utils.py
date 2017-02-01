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

main_doc_fields = ["doc_id", "title", "n_pages"]


def getCnx():
    u,p = utils.get_creds('MySQL')
    cnx = mysql.connector.connect(user=u, password=p, database=DB)
    return(cnx)


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


def docinfoFromMySQL(limit=0, fields="all", which="all"):
    """
    Pull document info from MySQL instance
    """
    u,p = utils.get_creds('MySQL')
    cnx = mysql.connector.connect(user=u, password=p, database=DB)
    cur = MySQLCursor(cnx)
    
    try:
    
        if limit==0:
            limit_text = ""
        else:
            limit_text = " LIMIT " + str(limit)
            
        if fields=="all":
            fields = main_doc_fields
        if type(fields) != list:
            fields = list(fields)
        for f in fields:
            if f not in main_doc_fields:
                err_msg = "Specified field '{}' not a valid field for docs".format(f)
                raise ValueError(err_msg)
                
        if which=="all":
            which_text = ""
        else:
            which_text = " WHERE doc_id IN "
            doc_id_list = ", ".join(["'" + str(did) + "'" for did in which])
            which_text = which_text + "(" + doc_id_list + ")"

        sqlq = "SELECT " + ", ".join(fields) + " FROM " + TABLE + limit_text + which_text
        cur.execute(sqlq)
        return(cursor_query_response_to_dict(cur))
    
    finally:
        cur.close()
        cnx.close()
    
    
def cursor_query_response_to_dict(cursor):
    """
    Turns cursor list-tuple response into a list-dict response;
    Exhausts the cursor
    """
    columns = cursor.column_names
    results = [{col : item for col,item in zip(columns, res)} for res in cursor.fetchall()]
    return(results)


def docinfoFromMySQLIter():
    """
    Return an iterator over the items in the MySQL db
    """
    pass


def dump_entries(cursor, entries):
    
    add_entry = ("INSERT INTO " + TABLE + " "
                 "(doc_id, title, n_pages) "
                 "VALUES (%(doc_id)s, %(title)s, %(n_pages)s)")
    
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