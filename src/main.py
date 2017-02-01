#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 10:26:48 2017

@author: immersinn
"""

import file_load
import pipelines


def main():
    docs = file_load.retrieve_docs()
    return(docs)