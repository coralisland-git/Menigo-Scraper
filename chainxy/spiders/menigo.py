# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import FormRequest

from scrapy.http import Request

from chainxy.items import ChainItem

from scrapy import signals

from scrapy.xlib.pydispatch import dispatcher

from selenium import webdriver

from lxml import etree

from lxml import html

import math

import time

import pdb

import unicodecsv as csv

from io import BytesIO

class Menigo(scrapy.Spider):

	name = 'menigo'

	domain = 'https://www.menigo.se'

	history = []

	output = []

	def __init__(self):

		pass
	
	def start_requests(self):
		# 3649
		limit = int(1611 / 24) + 1

		for idx in range(0, limit):
			skip = idx * 24
			count = (idx + 1) * 24
			# url = 'https://www.menigo.se/produkter/vin-sprit-och-starkol?count='+str(count)+'&infinitescroll=1&react&skip='+str(skip)+'&sortBy=popularity'
			url= 'https://www.menigo.se/produkter/dryck/kalla-drycker?count='+str(count)+'&infinitescroll=1&react&skip='+str(skip)+'&sortBy=popularity'
			yield scrapy.Request(url, callback=self.parse) 


	def parse(self, response):

		product_list = json.loads(response.body)['products']['products']

		for product in product_list:

			link = self.domain + product['url']

			if link not in self.history:

				self.history.append(link)

				yield scrapy.Request(link, callback=self.parse_detail)


	def parse_detail(self, response):

		item = ChainItem()

		data = response.xpath('//ul[@class="_2bt5aK"]//li')

		for prop in data:

			prop = self.eliminate_space(prop.xpath('.//text()').extract())

			item['Product_Name'] = ''.join(self.eliminate_space(response.xpath('//div[@class="_3a3aWs"]/h1//text()').extract()))

			item['Article_Number'] = ''.join(self.eliminate_space(response.xpath('//div[@class="_3a3aWs"]//div[@class="lUttE-"]//text()').extract()))

			if 'kategori' in prop[0].lower():

				item['Category'] = prop[1].encode('utf-8')

			if 'leveran' in prop[0].lower():

				item['Supplier_Name'] = prop[1].encode('utf-8')

			if 'producent' in prop[0].lower():

				item['Producer'] = prop[1].encode('utf-8')

			if 'ursprungsland' in prop[0].lower():

				item['Country'] = prop[1].encode('utf-8')

			if 'packning' in prop[0].lower():

				item['Package'] = prop[1].encode('utf-8')

			if 'alkoholprocent' in prop[0].lower():

				item['Alcohol_Percent'] = prop[1].encode('utf-8')

			if 'lev.artnr' in prop[0].lower():

				item['Volumn'] = prop[1].encode('utf-8')

		yield item

	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass


	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '' and self.validate(item) != ':':

	            tmp.append(self.validate(item))

	    return tmp
