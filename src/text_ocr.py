#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 17:02:14 2017

@author: immersinn
"""

import textract


def textFromPDF(pdf):
    """
    
    """
    text = textract.process(pdf, method="tesseract", language="eng")
    return(text)