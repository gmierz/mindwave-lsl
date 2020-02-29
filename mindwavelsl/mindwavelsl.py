"""
Used to synchronize Mindwave measurments with other tools
through LabStreamingLayer. 
"""
import json
import sys
import time

from mindwavelsl.parser import mwparser
from mindwavelsl.logger import MindwaveLogger
from mindwavelsl import MindwaveLSL

log = MindwaveLogger('mindwave-main')

def main():
	args = mwparser().parse_args()

	log.info("Checking args...")
	if args.mindwave_python_connect:
		if not args.device:
			raise Exception(
				"--device is required when using `mindwave` to connect. "
				"You might also need to use --headset-id."
			)

	mwlsl = MindwaveLSL(
		args.host,
		args.port,
		file_outlet_path=args.output,
		run_lsl=args.no_lsl,
		mindwave_python_connect=args.mindwave_python_connect,
		device=args.device,
		headset_id=args.headset_id,
		open_serial=args.no_open_serial
	)

	log.info("Setting up...")
	mwlsl.setup()
	mwlsl.write('{"enableRawOutput": true, "format": "Json"}')

	log.info("Running...")
	mwlsl.run()

if __name__=="__main__":
	main()
