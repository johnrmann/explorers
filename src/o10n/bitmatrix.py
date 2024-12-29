import ctypes
from ctypes import POINTER, c_int, c_char, c_uint16, Structure, byref

lib = ctypes.CDLL('./bin/compiled.so')

class Bitmatrix(Structure):
	__fields__ = [
		('data', POINTER(c_uint16)),
		('width', c_int),
		('height', c_int)
	]

lib.make_bitmatrix.argtypes = [c_int, c_int]
lib.make_bitmatrix.restype = POINTER(Bitmatrix)

lib.free_bitmatrix.argtypes = [POINTER(Bitmatrix)]
lib.free_bitmatrix.restype = None
