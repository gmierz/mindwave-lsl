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

	mwlsl = MindwaveLSL(args.host, args.port)

	log.info("Setting up...")
	mwlsl.setup_lsl()
	mwlsl.write('{"enableRawOutput": true, "format": "Json"}')

	log.info("Running...")
	mwlsl.run()

if __name__=="__main__":
	main()
