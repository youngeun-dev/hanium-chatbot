from flask import Flask
from pymongo import MongoClient
import requests


client = MongoClient('localhost', 27017)
db = client.chatbot
collection = db.performance
Poster=''
perf = collection.find({"poster":{"$exists":"true"}},{"poster":1})
for i in perf:
    Poster=i['poster']
    try:
        string = Poster.find(':')
        final = Poster[:string]+'s'+Poster[string:]
        collection.update_one({"poster":Poster},{ "$set": {"poster":final}})
    except:
        continue


