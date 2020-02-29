import collections
import json
import numpy as np
import os
import pylsl as lsl
import uuid

from mindwavelsl.connectors import TelnetConnector, MindwavePythonWrapper
from mindwavelsl.constants import (
	EXPECTED_FIELDS,
	MINDWAVE_PYTHON_ORIG,
	MINDWAVE_PYTHON_FORK
)
from mindwavelsl.logger import MindwaveLogger

log = MindwaveLogger("mindwave-outlet")


class MindwaveLSL(object):
	"""
	Acts as an interface to the telnet access point and
	provides this data in an LSL outlet.
	"""

	def __init__(
			self,
			host,
			port,
			file_outlet_path='',
			run_lsl=True,
			mindwave_python_connect=False,
			device='',
			headset_id='',
			open_serial=True
		):
		"""
		Initializes the MindwaveLSL outlet.

		:param str host: Host to find the data on.
		:param int port: Port to find the data on.
		:param str file_outlet_path: Path to where the data
			will be output, if not set, no data will be
			saved.
		:param bool run_lsl: If set to False, LSL outlet
			won't be created during the setup step.
		"""
		self.host = host
		self.port = port
		self.outlet = None
		self.file_outlet = None
		self.outlets = []

		# Standard settings
		self._outlet_uuid = str(uuid.uuid4())
		self._channels = []
		self._access_point = None
		self._file_outlet_path = file_outlet_path
		self._run_lsl = run_lsl

		# Mindwave-python settings
		self._mindwave_python_connect = mindwave_python_connect
		self._device = device
		self._headset_id = headset_id
		self._open_serial = open_serial

	def _check_started(self):
		"""
		Similar to started, but it raises an Excpetion
		if telnet wasn't setup.
		"""
		if not self.started():
			raise Exception(
				"Telnet access point was not started. Run `setup()` first."
			)
		return True

	def started(self):
		"""
		Returns true if started, false otherwise.
		"""
		return self._access_point != None

	def setup(self):
		"""
		Starts a telnet connection to the ThinkGear Controller,
		and prepares an outlet for the data.
		"""
		if self.started():
			return self._access_point

		# Prepare outlet
		log.info("Creating outlet and channels...")
		self._setup_channels()
		log.debug("Creating outlets...")

		if self._run_lsl:
			self._setup_lsl_outlet()
		if self._file_outlet_path:
			self._setup_file_outlet()

		if not self.outlets:
			raise Exception(
				"Cannot run since no outlet was created.")
		else:
			log.info("Mindwave outlets created")

		# Setup the Mindwave connector
		if self._mindwave_python_connect:
			try:
				import mindwavelsl.vendor.mindwave as mindwave
			except:
				raise Exception(
					"`mindwave` module could not be found. It needs to be "
					"installed manually from one of these two sources: \n%s\n%s" %
					(MINDWAVE_PYTHON_ORIG, MINDWAVE_PYTHON_FORK)
				)

			self._access_point = MindwavePythonWrapper(
				self._device, self._headset_id, self._open_serial
			)
		else:
			self._access_point = TelnetConnector(self.host, self.port)

		self._access_point.setup()

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

	def _setup_lsl_outlet(self):
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

		self.outlets.append(self.outlet)
		return self.outlet


	def _setup_file_outlet(self):
		"""
		Sets up the LSL output for the telnet data.
		"""
		self.file_outlet = FileOutlet(self._file_outlet_path)

		self.file_outlet.set_header(EXPECTED_FIELDS)
		self.file_outlet.setup_outlet()

		self.outlets.append(self.file_outlet)
		return self.file_outlet

	def write(self, data):
		"""
		Writes data to the connector.
		:param dict/str data: The data to send in either a
			dict or str form.
		"""
		self._check_started()

		try:
			self._access_point.write(data)
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
			response = self._access_point.read()
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
		if type(response) == list:
			# If the response is a list, then return it
			# immediately because it's already in sample form.
			return response

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

				sample = self.make_sample(response)

				for outlet in self.outlets:
					outlet.push_sample(sample)
			except KeyboardInterrupt as e:
				raise e	
			except Exception as e:
				log.error("Unknow error occured while running")
				log.error(
					"%s - %s" % (e.__class__.__name__, e)
				)	

class _Channel(object):
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


class FileOutlet(object):
	"""
	Used to output gathered data to a file.
	"""
	def __init__(self, path):
		"""
		Initialize the FileOutlet.

		:param str path: Path to the output location.
		"""
		self.path = path
		self.file = 'mindwave-output.csv'
		self._header = []
		self._filehandler = None

	def _sample_to_csv(self, sample):
		"""
		Converts a sample to a CSV entry.
		:param list sample: Sample to convert.
		"""
		return ",".join([str(s) for s in sample])

	def _make_dirs(self):
		"""
		Makes the output directory.
		"""
		if self.path.endswith('.csv'):
			path, file = os.path.split(self.path)
			self.path = path
			self.file = file
		os.makedirs(self.path, exist_ok=True)

	def set_header(self, header):
		"""
		Sets up the CSV file header.
		:param list header: Header for each of the data columns.
		"""
		self._header = header

	def setup_outlet(self):
		"""
		Sets up the file that data will be written to.
		"""
		if not self._header:
			raise Exception("FileOutlet CSV header is empty.")

		self._make_dirs()

		self._filehandler = open(os.path.join(self.path, self.file), "a", 5)
		self.push_sample(self._header)

	def push_sample(self, sample):
		"""
		Push a sample that conforms to the given header.
		:param list sample: Data sample to write.
		"""
		self._filehandler.write(self._sample_to_csv(sample) + "\n")
