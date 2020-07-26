#!/usr/bin/env python3 

from misc_util import *
from enum import Enum, auto
import math


#--------
class Var:
	def __init__(self, offset=-1):
		self.__offset = offset

	def offset(self):
		return self.__offset
	def _set_offset(self, offset):
		self.__offset = offset

	def __len__(self):
		return 0

class Byte(Var):
	def __init__(self, offset=0):
		super().__init__(offset=offset)
	def __len__(self):
		return 1
class Hword(Var):
	def __init__(self, offset=0):
		super().__init__(offset=offset)
	def __len__(self):
		return 2
class Word(Var):
	def __init__(self, offset=0):
		super().__init__(offset=offset)
	def __len__(self):
		return 4
class Dword(Var):
	def __init__(self, offset=0):
		super().__init__(offset=offset)
	def __len__(self):
		return 8

class Array(Var):
	def __init__(self, ElemType, ELEM_SIZE, NUM_ELEMS, offset=0):
		super().__init__(offset=offset)
		self.__ElemType, self.__ELEM_SIZE, self.__NUM_ELEMS \
			= ElemType, ELEM_SIZE, NUM_ELEMS

	def ElemType(self):
		return self.__ElemType
	def ELEM_SIZE(self):
		return self.__ELEM_SIZE
	def NUM_ELEMS(self):
		return self.__NUM_ELEMS

	def __len__(self):
		return (self.ELEM_SIZE() * self.NUM_ELEMS())

class Struct(Var):
	def __init__(self, layout):
		self.__layout = layout

		offset = 0

		for name in self.names():
			self[name]._set_offset(offset)
			offset += len(self[name])

	def __getitem__(self, key):
		return self.__layout[key]
	#def __setitem__(self, key, value):
	#	assert key in self.__layout
	#	self.__layout[key] = value
	def names(self):
		return {name for name in self.__layout}

	def __len__(self):
		return sum([len(self.__layout[name]) for name in self.names()])
#--------
