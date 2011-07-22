class Field(object):
	def parse(self, tree):
		raise Exception("You should have overridden this method.")

class XPathField(Field):
	def __init__(self, xpath):
		self.xpath = xpath
	def parse(self, tree):
		print "Parsing XPF"
		result = tree.xpath(self.xpath)
		if isinstance(result, list):
			return "".join(result)
		return result