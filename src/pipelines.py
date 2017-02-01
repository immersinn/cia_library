#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 09:21:25 2017

@author: immersinn
"""


import spacy
import textacy

import utils
import process_docs
import file_load


def pipe01(collection="presidents-daily-brief-1969-1977", 
           n_threads=8, batch_size=325):
    
#    # Preprocess Step:
#    preprocessor = lambda doc: process_docs.preprocessDoc(doc)
    
    
    
    # Load documents, initialize, preprocess
    docs = file_load.retrieve_docs(which="all")
    docs = process_docs.init_ciadocs(docs)
    
    # Define nlp pipeline
    nlp = spacy.load("en", add_vectors=False)
    nlp.pipeline = [nlp.tagger, nlp.parser]
    
    # Create textascy corpus from document, nlp
    corpus = textacy.Corpus(lang=nlp)
    corpus.add_texts(texts=[doc.content for doc in docs],
                     metadatas=[doc.meta for doc in docs],
                     n_threads=n_threads, batch_size=batch_size)
    
#    # Do all the other things
#    with utils.doc_stream(collection) as docs:
#        content_stream, metadata_stream = utils.proc_doc_iterator(docs,
#                                                                  tpp=preprocessor)
#        corpus = textacy.Corpus(lang=nlp, texts=content_stream, metadatas=metadata_stream)

    return(corpus)


def make_pipe01_dataset(name = "presidents-daily-brief-1969-1977"):
    corpus = pipe01(collection = name)
    name = "CORPUS_" + name + "_pipe01"
    utils.save_corpus(name, corpus)
    
    
if __name__=="__main__":
    make_pipe01_dataset()