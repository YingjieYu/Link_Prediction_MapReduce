#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: yuyingjie


Using two files users.json and hotels.json to model the bipartite graph, which has 
all the users on one side of the graph and all the hotels on the other side of the graph 
and an edge goes between user and hotel if a user has written a review for that hotel.
"""

import json, datetime
import os
import random
#import snap
from collections import defaultdict, Counter

def write_json(d, fname):
    with open(fname, 'w') as f:
        f.write(json.dumps(d))
        
def 