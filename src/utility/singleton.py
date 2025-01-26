def singleton(cls):
	instances = {}

	def reset_instance():
		if cls in instances:
			del instances[cls]

	def set_instance(instance):
		instances[cls] = instance

	def get_instance(*args, **kwargs):
		if cls not in instances:
			instances[cls] = cls(*args, **kwargs)
		return instances[cls]

	cls.reset_instance = reset_instance
	cls.set_instance = set_instance
	cls.get_instance = get_instance
	cls.get_instance.reset_instance = reset_instance
	cls.get_instance.set_instance = set_instance

	return get_instance
