import argparse

def mwparser():
	"""
	Used to parse arguments for the CLI version of `mindwavelsl`.
	"""
	parser = argparse.ArgumentParser(
		description="Run this tool to push Mind Wave Mobile 2 data from the "
					"ThinkGear Connector socket, to Lab Streaming Layer (LSL)."
	)
	parser.add_argument('--host', type=str, default='localhost',
						help='The host for the ThinkGear Connector.')
	parser.add_argument('--port', type=int, default=13854,
						help="The port for the ThinkGear Connector.")
	return parser
