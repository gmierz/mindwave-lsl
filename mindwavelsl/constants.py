import numpy as np

# Links to mindwave-python variants
MINDWAVE_PYTHON_ORIG = "https://github.com/BarkleyUS/mindwave-python"
MINDWAVE_PYTHON_FORK = "https://github.com/faturita/python-mindwave"

# This list holds the ordering of the samples pushed to LSL
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

# Mapping from LSL names to mindwave-python names and functions to retrieve them.
#
# Missing the `familiarity`, `rawEegMulti.*`, and `mentalEffort`
# fields.

def get_value(headset, field):
	"""
	Returns a value from a mindwave.Headset object.
	"""
	return getattr(headset, field, np.nan)

def get_wave_value(headset, field):
	"""
	Returns a value from the waves attribute in a
	mindwave.Headset object.
	"""
	return headset.waves.get(field, np.nan)

MINDWAVEPYTHON_MAPPINGS = {
	"rawEeg": (get_value, "raw_value"),
	"blinkStrength": (get_value, "blink"),
	"poorSignalLevel": (get_value, "poor_signal"),
	"eSense.attention": (get_value, "attention"),
	"eSense.meditation": (get_value, "meditation"),
	"eegPower.delta": (get_wave_value, "delta"),
	"eegPower.theta": (get_wave_value, "theta"),
	"eegPower.lowAlpha": (get_wave_value, "low-alpha"),
	"eegPower.highAlpha": (get_wave_value, "high-alpha"),
	"eegPower.lowBeta": (get_wave_value, "low-beta"),
	"eegPower.highBeta": (get_wave_value, "high-beta"),
	"eegPower.lowGamma": (get_wave_value, "low-gamma"),
	"eegPower.highGamma": (get_wave_value, "high-gamma")
}
