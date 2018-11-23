class Relay:
	def __init__(self, fullinit=False, database=None, ro=False):
		self.states = [False, False, False, False]

	def setEnabled(self, index, state):
		print("setting relay {} {}".format(index, ('off','on')[int(state)]))

	def save(self):
		pass

	def load(self):
		pass
