#!/usr/bin/env python3

from misc_util import *
from nmigen import *
import nmigen.tracer
from nmigen.hdl.rec import Record, Layout
from nmigen.asserts import Assert, Assume, Cover
from nmigen.asserts import Past, Rose, Fell, Stable

from enum import Enum, auto

#--------
class SigContrExtraArgs:
	#--------
	def __init__(self, *, name=None, reset=0, reset_less=False, attrs=None,
		decoder=None, src_loc_at=0):
		self.__name = name
		self.__reset = reset
		self.__reset_less = reset_less
		self.__attrs = attrs
		self.__decoder = decoder
		self.__src_loc_at = src_loc_at
	#--------
	def name(self):
		return self.__name
	def reset(self):
		return self.__reset
	def reset_less(self):
		return self.__reset_less
	def attrs(self):
		return self.__attrs
	def decoder(self):
		return self.__decoder
	def src_loc_at(self):
		return self.__src_loc_at
	#--------
#--------
class Packarr(ValueCastable):
	#--------
	def __init__(self, ELEM_WIDTH, SIZE, signed=False, extra_args=None):
		self.__ELEM_WIDTH = ELEM_WIDTH
		self.__SIZE = SIZE
		self.__extra_args = SigContrExtraArgs() \
			if extra_args == None \
			else extra_args

		shape = unsigned(self.ELEM_WIDTH() * self.SIZE()) \
			if not signed \
			else signed(self.ELEM_WIDTH() * self.SIZE())

		self.__sig \
			= Signal \
			(
				shape=shape,
				name=self.__extra_args.name(),
				reset=self.__extra_args.reset(),
				reset_less=self.__extra_args.reset_less(),
				attrs=self.__extra_args.attrs(),
				decoder=self.__extra_args.decoder(),
				src_loc_at=self.__extra_args.src_loc_at(),
			)
	#--------
	def ELEM_WIDTH(self):
		return self.__ELEM_WIDTH
	def extra_args(self):
		return self.__extra_args
	def sig(self):
		return self.__sig
	def shape(self):
		return self.sig().shape()
	#--------
	@staticmethod
	def to_sig(val):
		assert (isinstance(val, Signal) or isinstance(self, Packarr))

		return val \
			if isinstance(val, Signal) \
			else val.sig()
	#--------
	def eq(self, val):
		return self.sig().eq(Packarr.to_sig(val))

	@staticmethod
	def like(other, name=None, name_suffix=None, src_loc_at=0, **kwargs):

		if name is not None:
			new_name = str(name)
		elif name_suffix is not None:
			new_name = other.extra_args().name() + str(name_suffix)
		else:
			new_name = tracer.get_var_name(depth=src_loc_at + 2, 
				default="$like")

		kw \
			= dict \
			(
				ELEM_WIDTH=other.ELEM_WIDTH(),
				SIZE=len(other),
				extra_args=SigContrExtraArgs
					(
						name=new_name,
						src_loc_at=src_loc_at + 1,
					)
			)
		if isinstance(other, Packarr):
			kw["extra_args"] \
				= SigContrExtraArgs \
				(
					name=kw["extra_args"].name(),
					reset=other.extra_args().reset(),
					reset_less=other.extra_args().reset_less(),
					attrs=other.extra_args().attrs(),
					decoder=other.extra_args().decoder(),
					src_loc_at=kw["extra_args"].src_loc_at(),
				)
		kw.update(kwargs)

		return Packarr(**kw)

	#def as_unsigned(self):
	#	return \
	#		Packarr \
	#		(
	#			ELEM_WIDTH=self.ELEM_WIDTH(),
	#			SIZE=self.__SIZE,
	#			signed=False,
	#			extra_args=self.extra_args()
	#		)
	#def as_signed(self):
	#	return \
	#		Packarr \
	#		(
	#			ELEM_WIDTH=self.ELEM_WIDTH(),
	#			SIZE=self.__SIZE,
	#			signed=True,
	#			extra_args=self.extra_args()
	#		)
	#--------
	def __eq__(self, val):
		return (self.sig() == Packarr.to_sig(val))
	def __ne__(self, val):
		return (self.sig() != Packarr.to_sig(val))
	def __lt__(self, val):
		return (self.sig() < Packarr.to_sig(val))
	def __gt__(self, val):
		return (self.sig() > Packarr.to_sig(val))
	def __le__(self, val):
		return (self.sig() <= Packarr.to_sig(val))
	def __ge__(self, val):
		return (self.sig() >= Packarr.to_sig(val))
	#--------
	@ValueCastable.lowermethod
	def as_value(self):
		return self.sig()
	def __bool__(self):
		return bool(self.sig())
	def __len__(self):
		#return len(self.sig())
		return self.__SIZE
	def __repr__(self):
		return repr(self.sig())
	def __getitem__(self, key):
		return self.sig().word_select(key, self.ELEM_WIDTH())
	#--------
#--------
# A record type is composed of separate signals.  This allows setting the
# attributes of every signal.
class SplitRecord:
	#--------
	def __init__(self, fields: dict={}):
		self.__fields = fields
	#--------
	def fields(self):
		return self.__fields
	#--------
	def __getattr__(self, name):
		return self[name]
	def __getitem__(self, name):
		if name[0] == "_":
			return self.__dict__[name]
		else: # if name[0] != "_":
			return self.fields()[name]

	def __setattr__(self, name, val):
		self[name] = val
	def __setitem__(self, name, val):
		self.__check_val_type("SplitRecord.__setitem___()", val)

		if name[0] == "_":
			return self.__dict__[name]
		else: # if name[0] != "_":
			self.fields()[name] = val
	#--------
	#@ValueCastable.lowermethod
	#def as_value(self):
	#	return Cat(*self.flattened())
	def __len__(self):
		return len(Cat(*self.flattened()))
	#def __repr__(self):
	#--------
	def __check_val_type(self, prefix_str, val):
		assert (isinstance(val, Signal) or isinstance(val, Record)
			or isinstance(val, Packarr) \
			or isinstance(val, SplitRecord)), \
			psconcat(prefix_str, " Error:  Need a `Signal`, `Record`, "
				"`Packarr`, or `SplitRecord` for `val`, and `val`'s ",
				"type is \"", type(val), "\".")
	def flattened(self):
		ret = []
		for val in self.fields().values():
			self.__check_val_type("SplitRecord.flattened()", val)

			if isinstance(val, Signal) or isinstance(val, Record) \
				or isinstance(val, Packarr):
				#ret.append(SigContrBase.get_nmigen_val(val))
				ret.append(val)
			else: # if isinstance(val, SplitRecord):
				ret.append(val.flattened())
		return ret
	def cat(self):
		return eval(psconcat("Cat(" + ",".join(self.flattened()) + ")"))
	#--------
#--------
