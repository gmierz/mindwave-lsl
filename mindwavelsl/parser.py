import argparse

from mindwavelsl.constants import MINDWAVE_PYTHON_ORIG, MINDWAVE_PYTHON_FORK

def mwparser():
	"""
	Used to parse arguments for the CLI version of `mindwavelsl`.
	"""
	parser = argparse.ArgumentParser(
		description="Run this tool to push Mind Wave Mobile 2 data from the "
					"ThinkGear Connector socket, to Lab Streaming Layer (LSL)."
	)

	# Service-specific settings
	parser.add_argument('--no-lsl', action="store_false", default=True,
						help="Set this flag to disable LSL outlet.")
	parser.add_argument('--output', type=str, default='',
						help="Path to output data to, can include a CSV filename.")

	# Telnet connection parameters
	parser.add_argument('--host', type=str, default='localhost',
						help='The host for the ThinkGear Connector.')
	parser.add_argument('--port', type=int, default=13854,
						help="The port for the ThinkGear Connector.")

	# Mindwave-python connection parameters.
	parser.add_argument('--mindwave-python-connect', action="store_true", default=False,
						help="Set this to connect to Mindwave headset using mindwave-python "
						"(through the module `mindwave`). It needs to be installed manually, "
						"and instructions can be found here: %s. A more up-to-date version "
						"exists here as well: %s. Must set --device and --headset-id to use."
						% (MINDWAVE_PYTHON_ORIG, MINDWAVE_PYTHON_FORK))
	parser.add_argument('--device', type=str, default='',
						help="Set this to the device of the headset to record i.e. /dev/tty.MindWave2.")
	parser.add_argument('--headset-id', type=str, default='',
						help="Set this to the headset-id of the headset to record.")
	parser.add_argument('--no-open-serial', action="store_false", default=True,
						help="If set, then `open_serial` in mindwave.Headset will be set "
						"to False.")

	return parser
