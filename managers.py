from lxml.html import parse

class URLRetrieveManager(object):
	def __init__(self, url):
		self.url = url
	
	def scrape_as(self, model_class):
		return model_class(parse(self.url))