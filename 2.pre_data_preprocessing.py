#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  4 14:07:30 2018

@author: yuyingjie


Using the reviews.json to create two more files one for users/authors and the other for hotels.
 The users.json had the following fields:
1. AuthorID ( a unique ID assigned by us)
2. ReviewCount (aggregation of all the re- views written by this author identified by Name/ID)
3. Last Review Date( date of the last review written by this author/user)
4. UserLocation

The hotels.json file on the other hand had the following fields:
1. HotelID
2. ReviewCount (aggregation of all the re- views written for this Hotel identified by ID)
3. HotelLocation
"""

import glob, json
import dateutil.parser
from collections import Counter

def write_json(d, fname):
    with open(fname, 'w') as f:
        f.write(json.dumps(d))
        
def make_init_user_hotel(reviews_it):
    userid_list=[]
    hotelid_list = []
    user_date={}
    for review, key in reviews_it.items():
        try:
            user_date[key['Author']].append(key['Date'])
        except:
            user_date[key['Author']]=[]
        userid_list.append(key['Author'])
        hotelid_list.append(key['HotelID'])
    u_c = Counter(userid_list)
    h_c = Counter(hotelid_list)
    return u_c,h_c,user_date

def make_user_list(review_json, user_json,date_json, hotel_json):
    user_loc = {}
    hotels = {}
    for review, key in review_json.items():
       userid=key['Author']
       user_loc[userid] = {'AuthorID': key['Author'],
               'ReviewCount':user_json[userid],
               'LastReviewDate':max(date_json[userid]) if date_json[userid] else -1,
               'UserLocation': key['Author Location']}
       hotelid = key["HotelID"]
       hotels[hotelid] = {"HotelID": key["HotelID"],
                           "ReviewCount": hotel_json[hotelid],
                           "HotelLocation": key["HotelLocation"]}
    
    write_json(user_loc, "./data/created/users.json")
    write_json(hotels, "./data/created/hotels.json")    

def main_creator():
    reviews_it={}
    with open('./data/created/review.json') as f:
        reviews_it=json.load(f)
    user_json, hotel_json, date_json = make_init_user_hotel(reviews_it)
    make_user_list(reviews_it, user_json, date_json, hotel_json)
    
if __name__ == '__main__':
    main_creator()

       