import urllib
from bs4 import BeautifulSoup
from lxml import html
import xmltodict, json
from pprint import pprint
import re
import requests
from lxml import *
from collections import defaultdict as dt

def scrape_it(url):

	InfoDict = dt(list)

	raw_feed = urllib.request.urlopen(url)
	html_soup = BeautifulSoup(raw_feed, 'html.parser')
	
	
	InfoDict["Title"] = html_soup.title.string
	InfoDict["StoryLink"] = url
	InfoDict["Date"] = str(html_soup.find('time', attrs = {'class':'buzz-timestamp__time js-timestamp__time'}).string).strip("\n").strip()
	InfoDict["WriterName"] = html_soup.find('div', attrs = {'class':'byline vignette xs-flex-align-center xs-flex xs-mb1'}).div.a['title']
	
	if html_soup.find('span', attrs = {'class':'js-subbuzz__title-text'}) is not None:
		InfoDict["Short Description"] = html_soup.find('span', attrs = {'class':'js-subbuzz__title-text'}).string

	complete_article = html_soup.find('article', attrs = {'class':'buzz buzz--list clearfix'})

	sub_section_list = list()

	for c in complete_article.contents:
		
		parsed = BeautifulSoup(str(c), 'html.parser')
		
		section = parsed.findAll('div', attrs = {'class':'subbuzz subbuzz-image xs-mb4 xs-relative xs-mb1'})

		text_section = parsed.findAll('div', attrs = {'class':'subbuzz subbuzz-text xs-mb4 xs-relative'})

		for x in section:
			parsed_section = BeautifulSoup(str(x),'html.parser')

			value = list()

			if x.findChildren('figure'):
				value.append({"content":parsed_section.figure.div.div.img['data-src'], "type": "figure"})
			
			if x.findChildren('h3'):
				value.append({"content":parsed_section.h3.span.string, "type":"figure-text"})

			if len(value):
				sub_section_list.append(value)						

		for x in text_section:
			
			parsed_text_section	= BeautifulSoup(str(x),'html.parser')

			value = list()

			if x.findChildren('h3'):
				value.append({"content":parsed_section.h3.span.string, "type":"figure-text"})

			if len(value):
				sub_section_list.extend(value)						


	InfoDict["blocks"].append(sub_section_list)	

	return InfoDict


if __name__=="__main__":

	Link = "https://www.buzzfeed.com/index.xml"

	page = urllib.request.urlopen(Link)

	soup = BeautifulSoup(page, 'lxml-xml')

	Output = xmltodict.parse(str(soup))

	#print (json.dumps(Output, sort_keys = True, indent = 4, separators = (',',':') ))

	myList = list()

	count = 0

	for link in soup.find_all('link'):
		var = xmltodict.parse(str(link))
		for k, v in var.items():
			count+=1
			if count>3:
				myList.append(scrape_it(str(v)))


	Output = open("Output.txt", 'w')

	Output.write(json.dumps(myList, sort_keys = True, indent = 4, separators = (',',':')))

	Output.close()
