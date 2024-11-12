"""
Utility functions for lists.
"""

def next_index_with_item(items, item, ptr):
	"""
	Find the index of the first occurance of an item in a list after a given
	position.
	"""
	for i in range(ptr, len(items)):
		if items[i] == item:
			return i
	return -1

def prev_index_with_item(items, item, ptr):
	"""
	Find the index of the first occurance of an item in a list before a given
	position.
	"""
	ptr -= 1
	while ptr >= 0:
		if items[ptr] == item:
			return ptr
		ptr -= 1
	return -1
