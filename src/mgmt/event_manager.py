class EventManager:
	_queue: list[tuple[str, any]]

	def __init__(self):
		self.listeners = {}
		self.all_listeners = {}
		self._queue = []

	def sub(self, event_type, listener):
		"""
		Subscribe a listener to an event.
		"""
		if event_type not in self.listeners:
			self.listeners[event_type] = set()
		if listener not in self.all_listeners:
			self.all_listeners[listener] = 0
		self.listeners[event_type].add(listener)
		self.all_listeners[listener] += 1

	def unsub(self, event_type, listener):
		"""
		Unsubscribe a listener from an event.
		"""
		if event_type in self.listeners:
			self.listeners[event_type].remove(listener)
			self.all_listeners[listener] -= 1

	def is_subbed(self, listener):
		"""
		Returns true if the listener is subscribed to at least one event.
		"""
		if listener not in self.all_listeners:
			return False
		return self.all_listeners[listener] != 0

	def is_subbed_to_event(self, event_type, listener):
		"""
		Returns true if the listener is subscribed to a specific event.
		"""
		if event_type not in self.listeners:
			return False
		event_listeners = self.listeners[event_type]
		return listener in event_listeners

	def pub(self, event_type, data=None):
		"""
		Publish an event with a data payload.
		"""
		self._queue.append((event_type, data))

	def tick(self, dt: float, utc: float):
		"""
		Process events from the last tick in this one.
		"""
		for event_type, data in self._queue:
			if event_type in self.listeners:
				for listener in self.listeners[event_type]:
					listener.update(event_type, data)
		self._queue = []
