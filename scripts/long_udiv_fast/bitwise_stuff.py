#!/usr/bin/env python3

def to_bits(x, WIDTH=0, dbg=""):
	assert type(x) == int, "Need `x` to be an `int`:  {}".format(type(x))
	assert x >= 0, "Need `x` to be >= 0:  {}".format(x)

	assert type(WIDTH) == int, \
		"Need `WIDTH` to be an `int`: {}".format(type(WIDTH))
	assert WIDTH > 0, "Need `WIDTH` to be > 0:  {}".format(WIDTH)

	b = bin(x)

	if len(dbg) > 0:
		print("to_bits() {}:  {} {}; {} {}".format(dbg, x, WIDTH, b,
			b[2:]))
	temp = list(b[2:])
	temp.reverse()

	# Convert every element to an integer
	ret = [int(elem) for elem in temp]

	if WIDTH != 0:
		for i in range(len(ret) - 1, WIDTH - 1):
			ret.append(0)

	return ret

def from_bits(x):
	assert type(x) == list, "Need `x` to be a `list`:  {}".format(type(x))
	ret = "0b"

	#temp = x
	temp = [elem for elem in x]
	temp.reverse()

	for val in temp:
		ret += str(val)

	ret = int(ret, 2)
	return ret
