import collections
import json
import numpy as np
import pylsl as lsl
import uuid
from telnetlib import Telnet

from mindwavelsl.logger import MindwaveLogger

log = MindwaveLogger("mindwave-outlet")

EXPECTED_FIELDS = [
	"rawEegMulti.ch1",
	"rawEegMulti.ch2",
	"rawEegMulti.ch3",
	"rawEegMulti.ch4",
	"rawEegMulti.ch5",
	"rawEegMulti.ch6",
	"rawEegMulti.ch7",
	"rawEegMulti.ch8",
	"rawEeg",
	"familiarity",
	"mentalEffort",
	"blinkStrength",
	"poorSignalLevel",
	"eSense.attention",
	"eSense.meditation",
	"eegPower.delta",
	"eegPower.theta",
	"eegPower.lowAlpha",
	"eegPower.highAlpha",
	"eegPower.lowBeta",
	"eegPower.highBeta",
	"eegPower.lowGamma",
	"eegPower.highGamma",
]


class MindwaveLSL(object):
	"""
	Acts as an interface to the telnet access point and
	provides this data in an LSL outlet.
	"""

	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.outlet = None

		self._outlet_uuid = str(uuid.uuid4())
		self._channels = []
		self._access_point = None

	def _check_started(self):
		"""
		Similar to started, but it raises an Excpetion
		if telnet wasn't setup.
		"""
		if not self.started():
			raise Exception(
				"Telnet access point was not started. Run `setup_lsl()` first."
			)
		return True

	def started(self):
		"""
		Returns true if started, false otherwise.
		"""
		return self._access_point != None

	def setup_lsl(self):
		"""
		Starts a telnet connection to the ThinkGear Controller,
		and prepares an outlet for the data.
		"""
		if self.started():
			return self._access_point

		# Prepare outlet
		log.info("Creating outlet and channels...")
		self._setup_channels()
		log.debug("Creating outlet...")
		self._setup_outlet()
		log.info("Mindwave outlet created")

		# Setup telnet
		log.info("Connecting to ThinkGear Connector...")
		self._access_point = Telnet(self.host, self.port)
		log.info("Connected with telnet")

		return self._access_point

	def _setup_channels(self):
		"""
		Sets up all the channels that will be recorded.
		"""
		for field in EXPECTED_FIELDS:
			unit = 'a.u.'
			if field == 'rawEeg':
				unit = 'microvolts'
			self._channels.append(_Channel(field, "EEG", unit))

		return self._channels

	def _setup_outlet(self):
		"""
		Sets up the LSL output for the telnet data.
		"""
		stream_info = lsl.StreamInfo(
			name="Mindwave",
			type="Gaze",
			channel_count=len(self._channels),
			channel_format=lsl.cf_double64,
			source_id=self._outlet_uuid,
		)
		stream_info.desc().append_child_value("mindwavelsl-version", "1.0")
		xml_channels = stream_info.desc().append_child("channels")
		for chan in self._channels:
			chan.append_to(xml_channels)

		self.outlet = lsl.StreamOutlet(stream_info)

		return self.outlet

	def write(self, data):
		"""
		Writes data to the telnet connection.
		:param dict/str data: The data to send in either a
			dict or str form.
		"""
		self._check_started()

		try:
			if type(data) == dict:
				data = json.dumps(data)
			self._access_point.write(str.encode(data))
		except Exception as e:
			log.error(
				"Unknow error occured while WRITING this response: "
				"%s" % data
			)
			log.error(
				"%s - %s" % (e.__class__.__name__, e)
			)

	def read(self, read_until="\r"):
		"""
		Pulls data from the telnet connection until `\r`
		is encountered.
		:param str read_until: Read data until we find this string.
		"""
		self._check_started()

		response = None
		try:
			response = self._access_point.read_until(b"\r")
		except KeyboardInterrupt as e:
			raise e
		except Exception as e:
			log.error("Unknow error occured while READING")
			log.error(
				"%s - %s" % (e.__class__.__name__, e)
			)
		return response

	def make_sample(self, response):
		"""
		Builds up a sample using the channels as a
		reference for what fields we should look for.
		"""
		sample = []
		for chan in self._channels:
			sample.append(response.get(chan.metric, np.nan))
		if response.get("poorSignalLevel", 0) == 200:
			log.warning("Poor signal quality, check headset fitting...")
		else:
			log.debug(sample)
		return sample

	def run(self):
		"""
		Starts two threads here. 
		"""
		# 2 threads, one manager, one pusher
		while True:
			try:
				response = self.read()
				if not response:
					continue

				sample = self.make_sample(
					flatten(json.loads(response))
				)

				self.outlet.push_sample(sample)
			except KeyboardInterrupt as e:
				raise e	
			except Exception as e:
				log.error("Unknow error occured while running")
				log.error(
					"%s - %s" % (e.__class__.__name__, e)
				)	

class _Channel:
	"""
	Container class for each channel to simplify setup,
	data parsing, and generation.
	"""
	def __init__(self, metric, metatype, unit):
		self.label = "Fp1"
		self.metric = metric
		self.metatype = metatype
		self.unit = unit

		if metric != "rawEeg":
			self.label = "Fp1-%s" % metric

	def append_to(self, channels):
		chan = channels.append_child("channel")
		chan.append_child_value("label", self.label)
		chan.append_child_value("type", self.metatype)
		chan.append_child_value("unit", self.unit)


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
