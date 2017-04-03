# -*- coding: utf-8 -*-


import tweepy
from tweepy import OAuthHandler
import json
from pprint import pprint
import os
import pandas as pd
import time

consumer_key = 'consumer key'
consumer_secret = 'consumer passowrd'
access_token = 'access token'
access_secret = 'access secre'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth, wait_on_rate_limit= True)

os.chdir("path to file")
os.getcwd()

# Twitter Extraction
companynames=["Staples","Starbucks","TiffanyAndCo"]

for company in companynames:
    print("{}: Starting".format(company))    
    exec("{} = pd.DataFrame()".format(company))
    i=1
    for status in tweepy.Cursor(api.user_timeline, id=company).items(99999):
        try:        
            exec("{}.loc[i,\"CreatedAT\"]=str(status.created_at)".format(company))  
            exec("{}.loc[i,\"TEXT\"]=status.text".format(company))
            exec("{}.loc[i,\"FavouriteCount\"]=status.favorite_count".format(company))
            exec("{}.loc[i,\"ReTweetCount\"]=status.retweet_count".format(company))
            exec("{}.loc[i,\"PhotoURL\"]=status.entities[\"media\"][0][\"media_url\"]".format(company))
        except KeyError:
            pass
        except tweepy.error.TweepError:
            print("Rate Limit of Twitter API reached: Wait for 960 Seconds")            
            time.sleep(960)
        i=i+1
        if (str(status.created_at)[0:7] == "2016-03"):
            break
    exec("{0}.to_csv(\"E:/USF/Independent CSR/{1}.csv\", encoding='utf-8')".format(company,company))
    print("{}: Successfully Done".format(company))

# Twitter Extraction for one company    
ebay=pd.DataFrame()
i=1
for status in tweepy.Cursor(api.user_timeline, id="ebay").items(99999):
    try:        
         ebay.loc[i,"CreatedAT"]=str(status.created_at)
         ebay.loc[i,"TEXT"]=status.text
         ebay.loc[i,"FavouriteCount"]=status.favorite_count
         ebay.loc[i,"ReTweetCount"]=status.retweet_count
         ebay.loc[i,"PhotoURL"]=status.entities["media"][0]["media_url"]
    except KeyError:
        pass
    i=i+1
    if (str(status.created_at)[0:7] == "2016-03"):
        break
    
ebay.to_csv("E:\USF\Independent CSR\ebay.csv", encoding='utf-8')


# Facebook extraction

import facebook
import requests

access_token ="EAACEdEose0cBAB1lAZAYGuRcasN1ZBdNB0ZC5DDqBbwrxsU7OClxzYME3zDlbsYAFYiZCAGyZAPTFBHmZAL2KD8uZBxAmwTc8uyVdWSZBRcCBQY5oaUqrG77Hl2Tz8jiJ76ZBr281Mh5OgwhBIaBGIi7eWlaIF8Dc9WOIGcbh1lrrKgZDZD"

user = 'dollartree'

graph = facebook.GraphAPI(access_token)
profile = graph.get_object(user)
#posts = graph.get_connections(profile['id'], 'posts')
posts = graph.get_connections(user,'posts',  fields='message,created_time,likes.summary(true),shares,link')

dollartreeFB=pd.DataFrame()
for post in range(0,20):
    try:
        dollartreeFB.loc[post,"PostedAt"]=posts['data'][post]['created_time']
        dollartreeFB.loc[post,"Text"]=posts['data'][post]['message']
        dollartreeFB.loc[post,"LikesCount"]=posts['data'][post]['likes']['summary']['total_count']
        dollartreeFB.loc[post,"ShareCount"]=posts['data'][post]['shares']['count']
        dollartreeFB.loc[post,"Post Link"]=posts['data'][post]['link']
    except KeyError:
        pass

dollartreeFB.to_csv("E:\USF\Independent CSR\dollartreeFB.csv", encoding='utf-8')


