#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 17:15:38 2017

@author: Santhosh
"""

from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import feedParser
import pika
import json

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('url')
    
def handleException():
    abort(404, message = "Unable to Parse RSS")

def postInQueue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='feed_crawler')
    channel.basic_publish(exchange='',
                      routing_key='feed_crawler',
                      body=json.dumps(message),
                      properties=pika.BasicProperties(
                     delivery_mode = 2))
    connection.close()

class FeedParser(Resource):
    def post (self):
        result = {}
        args = parser.parse_args()
        url = args['url']
        try :
            feedData = feedParser.processFeed(url)
        except:
            handleException()
        result['entries'] = len(feedData['entries'])
        result['title'] = feedData['feed']['title']
        result['link'] = feedData['feed']['link']
        entriesList = [] 
        for post in feedData.entries:
            postMap = {}
            postMap['title'] = post.title
            postMap['link'] = post.link
            postMap['publishDate'] = post.published
            postMap['author'] = post.author
            postMap['summary'] = post.summary
            entriesList.append(postMap)
            postInQueue(postMap)
        result['feeds'] = entriesList
        return entriesList

api.add_resource(FeedParser , '/feedPraser')

if __name__ == '__main__':
    app.run(debug=True)