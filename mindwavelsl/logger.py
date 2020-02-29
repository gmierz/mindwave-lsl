import logging

logging.basicConfig(
	level=logging.INFO,
	format='[%(asctime)-15s][%(levelname)-8s] %(name)-12s - %(message)s',
	datefmt='%H:%M:%S'
)

class MindwaveLogger():

	def __init__(self, name, level=logging.INFO):
		self.logger = logging.getLogger(name)

	def debug(self, msg):
		self.logger.debug(msg)

	def info(self, msg):
		self.logger.info(msg)

	def warning(self, msg):
		self.logger.warning(msg)

	def error(self, msg):
		self.logger.error(msg)
