#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 16:44:01 2017

@author: Santhosh
"""
import feedparser

def processFeed( url):
    feeds = feedparser.parse(url)
    return feeds
