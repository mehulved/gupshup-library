#!/usr/bin/env python

""" 
This application fetches feeds from cyclists.in website's events page and parses it to obtain date and title of each event 

Credits:
http://snippets.dzone.com/posts/show/885
http://www.feedparser.org/
"""

# We will use the fantastic feedparser library to parse the feeds
import feedparser

def getFeed(rsslink):
	"""
	We will fetch the feeds from the RSS given RSS link and return a list of all the events.
	"""
	cyc_feed = feedparser.parse(rsslink)

	# This list will store the title from each entry in the feed
	feed_item = []

	for feed in cyc_feed['entries']
		feed_item.append(feed['title'])
	
	return feed_item

def storeMsg(feed_item):
	f = open('msgFile.txt', 'w')

	for item in feed_item:
		f.write(item+"\n")

	f.close()
