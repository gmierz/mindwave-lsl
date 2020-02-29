import numpy as np
import pyxdf
from matplotlib import pyplot as plt

# File to test
TEST_FILE = 'C:\\Recordings\\CurrentStudy\\exp4\\untitled.xdf'

# Load it and get the channels
data = pyxdf.load_xdf()
channels = data[0][0]['info']['desc'][0]['channels'][0]

# Get all the channel names
channames = []
for channel in channels['channel']:
	print(channel)
	channames.append(channel['label'][0])
print(channames)

# Get the channel for the Mindwave raw data in `rawEeg`
raw_channel = "Fp1"
chanind = [c for c,n in enumerate(channames) if n == raw_channel][0]
print("rawEeg channel index:" % chanind)

# Gather all the rawEeg data and plot it
timeseries = data[0][0]['time_series']
raweeg = []
for row in timeseries:
	if np.isnan(row[chanind]): continue
	raweeg.append(row[chanind])

plt.plot(raweeg)
plt.show()
