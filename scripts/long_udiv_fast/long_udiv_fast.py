#!/usr/bin/env python3

from misc_util import *
from bitwise_stuff import *

def long_udiv_fast(WIDTH, x, y):
	#--------
	class Loc:
		#--------
		CHUNK_WIDTH = 3
		@staticmethod
		def chunk_t(x=0):
			return to_bits(x=x, WIDTH=Loc.CHUNK_WIDTH)

		TEMP_T_WIDTH = CHUNK_WIDTH * ((WIDTH // CHUNK_WIDTH) + 2)
		#TEMP_T_WIDTH = Loc.CHUNK_WIDTH * ((WIDTH // Loc.CHUNK_WIDTH) + 1)
		@staticmethod
		def temp_t(x=0):
			return to_bits(x=x, WIDTH=Loc.TEMP_T_WIDTH)

		NUM_CHUNKS = TEMP_T_WIDTH // CHUNK_WIDTH
		#--------

		#--------
		GT_VEC_WIDTH = 2 ** CHUNK_WIDTH
		@staticmethod
		def gt_vec_t(x=0):
			return to_bits(x=x, WIDTH=Loc.GT_VEC_WIDTH)

		@staticmethod
		def bsearch(gt_vec):
			z = Loc.GT_VEC_WIDTH // 2
			#z = len(gt_vec) // 2
			m = z

			while z > 0:
				temp = z // 2
				old_z = z
				z = temp

				if old_z == 1:
					temp = 1

				if gt_vec[m] == 1:
					m -= temp
				elif old_z > 1:
					m += temp

			return Loc.chunk_t(m)

		# 2 ** 8 = 256 entries
		BSEARCH_LUT_SIZE = 2 ** GT_VEC_WIDTH

		@staticmethod
		def BSEARCH_LUT():
			return [Loc.bsearch(Loc.gt_vec_t(x=i))
				for i in range(Loc.BSEARCH_LUT_SIZE)]
		#--------

		#--------
		Y_MULT_LUT_SIZE = 2 ** CHUNK_WIDTH

		@staticmethod
		def Y_MULT_LUT():
			return [y * i for i in range(Loc.Y_MULT_LUT_SIZE)]
		#--------
	#--------

	#--------
	BSEARCH_LUT = Loc.BSEARCH_LUT()

	temp_x = Loc.temp_t(x=x)

	#Y_MULT_LUT = [Loc.temp_t(x=y * i)
	#	for i in range(Loc.Y_MULT_LUT_SIZE)]
	Y_MULT_LUT = Loc.Y_MULT_LUT()
	#--------

	#--------
	# Iteration variables
	prev = 0
	chunk_high = Loc.TEMP_T_WIDTH - 1
	chunk_low = chunk_high - (Loc.CHUNK_WIDTH - 1)

	quot_var = Loc.temp_t()
	rema_var = Loc.temp_t()
	temp_rema_var = []

	#gt_vec = Loc.gt_vec_t()
	#--------

	#--------
	for i in range(Loc.NUM_CHUNKS):
		#--------
		prev = i - 1
		#--------

		#--------
		# Shift in the current chunk of `temp_x`
		temp_rema_var = temp_x[chunk_low : chunk_high + 1] + rema_var

		rema_var = temp_rema_var[0 : len(rema_var)]
		rema_var_int = from_bits(rema_var)
		#--------

		#--------
		gt_vec = [1 if (Y_MULT_LUT[j] > rema_var_int) else 0
			for j in range(Loc.GT_VEC_WIDTH)]

		quot_chunk = BSEARCH_LUT[from_bits(gt_vec)]
		#--------

		#--------
		quot_var[chunk_low : chunk_high + 1] = quot_chunk

		rema_var_int = rema_var_int - Y_MULT_LUT[from_bits(quot_chunk)]

		rema_var = Loc.temp_t(x=rema_var_int)
		#--------

		#--------
		chunk_high -= Loc.CHUNK_WIDTH
		chunk_low -= Loc.CHUNK_WIDTH
		#--------

	#--------

	#--------
	return \
	{
		"quot": from_bits(quot_var),
		"rema": from_bits(rema_var)
	}
	#--------


def test_long_udiv(WIDTH):
	for x in range(1 << WIDTH):
		for y in range(1, 1 << WIDTH):
			to_test = long_udiv_fast(WIDTH=WIDTH, x=x, y=y)
			oracle \
			= {
				"quot": x // y,
				"rema": x % y
			}
			#if to_test != oracle:
			print("{} / {}:  {}, {}:  {}".format(x, y, to_test, oracle,
				to_test == oracle))
			#print("\n\n", end="")

test_long_udiv(WIDTH=8)
