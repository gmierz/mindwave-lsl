import collections
import json
from telnetlib import Telnet

try:
	import mindwavelsl.vendor.mindwave as mindwave
except:
	pass

from mindwavelsl.logger import MindwaveLogger
from mindwavelsl.constants import EXPECTED_FIELDS, MINDWAVEPYTHON_MAPPINGS

log = MindwaveLogger('mindwave-connector')


class MindwavePythonWrapper(object):
	"""
	Wrapper class for the `mindwave` module. Not fully tested.
	"""

	def __init__(self, device, headset_id, open_serial):
		"""
		Initializes the MindwavePythonWrapper.

		:param str device: Path to device file.
		:param str headset_id: ID of the headset.
		:param bool open_serial: If set to false then,
			the serial connection won't be opened.
		"""
		self._device = device
		self._headset_id = headset_id
		self._open_serial = open_serial

		self.headset = None

	def setup(self):
		"""
		Sets up the mindwave.Headset object.
		"""
		log.info("Connecting to headset using mindwave-python...")
		self.headset = mindwave.Headset(
			self._device,
			headset_id=self._headset_id,
			open_serial=self._open_serial
		)
		self.headset.connect()
		log.info("Connected to headset through mindwave-python")

	def read(self):
		"""
		Reads from the connection. Returns a sample whose ordering is based
		on the `constants.EXPECTED_FIELDS` list.
		"""
		def _default_val(headset, field):
			return np.nan

		sample = []
		for field in EXPECTED_FIELDS:
			func, field = MINDWAVEPYTHON_MAPPINGS.get(field, (_default_val, ""))
			sample.append(func(self.headset, field))

		return sample

	def write(self, data):
		"""
		Used to write to the connect, but it's disabled for mindwave.Headset.
		"""
		log.warning("Cannot write to `mindwave` connection")


class TelnetConnector(object):
	"""
	Used to connect, and read/write with the Telnet connection.
	"""
	def __init__(self, host, port):
		"""
		Initializes the connector.
		:param str host: Host to connect to.
		:param int port: Port to connect to on host.
		"""
		self.host = host
		self.port = port
		self.connection = None

	def setup(self):
		"""
		Starts the telnet connection.
		"""
		log.info("Connecting to ThinkGear Connector...")
		self.connection = Telnet(self.host, self.port)
		log.info("Connected with telnet")

	def read(self):
		"""
		Read from the connection until `\\r` is found.
		"""
		return flatten(json.loads(
			self.connection.read_until(b"\r")
		))


	def write(self, data):
		"""
		Writes to the connection.
		"""
		if type(data) == dict:
			data = json.dumps(data)
		self.connection.write(str.encode(data))


def flatten(d, parent_key='', sep='.'):
	"""
	Used to flatten the response and make it simpler to
	parse into an LSL sample.
	"""
	items = []
	for k, v in d.items():
		new_key = parent_key + sep + k if parent_key else k
		if isinstance(v, collections.MutableMapping):
			items.extend(flatten(v, new_key, sep=sep).items())
		else:
			items.append((new_key, v))
	return dict(items)
