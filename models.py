from fields import Field

class Options(object):
	def __init__(self):
		self.fields = {}

class MetaModelBase(type):
	def __new__(cls, name, bases, attrs):
		print "CREATING", name
		new_class = super(MetaModelBase, cls).__new__(cls, name, bases, attrs)

		if not hasattr(new_class, '_meta'):
			new_class.add_to_class('_meta', Options())
		for obj_name, obj in attrs.items():
			if not obj_name.startswith("_") and isinstance(obj, Field):
				new_class._meta.fields[obj_name] = obj
				print "\tADDED", obj_name
		return new_class

	def add_to_class(cls, name, value):
		if hasattr(value, 'contribute_to_class'):
			value.contribute_to_class(cls, name)
		else:
			setattr(cls, name, value)

class GroupItem(object):
	def __setattr__(self, key, val):
		self.__dict__[key] = val

class Group(Field):
	__metaclass__ = MetaModelBase

	def parse(self, tree):
		result = []
		for tree_item in tree:
			item = GroupItem()
			for obj_name, obj in self._meta.fields.items():
				item.__setattr__(obj_name, obj.parse(tree_item))
			result.append(item)
		return result
	
class XPathGroup(Group):
	def __init__(self, xpath):
		self.xpath = xpath

	def parse(self, tree):
		return super(XPathGroup, self).parse(tree.xpath(self.xpath))

class Model(object):
	__metaclass__ = MetaModelBase
	def __init__(self, tree):
		self.parse(tree)

	def parse(self, tree):
		for obj_name, obj in self._meta.fields.items():
			setattr(self, obj_name, obj.parse(tree))
