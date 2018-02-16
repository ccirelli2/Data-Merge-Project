# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 22:32:56 2018

@author: Chris.Cirelli
"""

# Import Packages

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re

    
Url = 'http://scip.cvstarrco.corp/scip/DNB/Product/42973875'



html = urlopen(Url)

#bsObj = BeautifulSoup(html.read(), 'lxml')
    
# Scrape Only News Article Links
#Links = bsObj.findAll('a', {'href':re.compile('\/eeoc\/newsroom\/release\/.*\.cfm')})