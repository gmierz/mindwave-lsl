import mindwavelsl
import numpy as np
import os
import win32api
from win32api import GetSystemMetrics


def move_mouse(x, y):
	win32api.SetCursorPos((x,y))


width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
print("Width =", width)
print("Height =", height)

mwlsl = mindwavelsl.MindwaveLSL('localhost', 13854)
mwlsl.setup()
mwlsl.write('{"enableRawOutput": true, "format": "Json"}')

prevatt = -1
prevmed = -1
currpos = [1200,1200]
while True:
	try:
		data = mwlsl.make_sample(mwlsl.read())
	except KeyboardInterrupt:
		raise
	except:
		continue

	# Check pos 13, 14 for attention, meditation
	if any([np.isnan(data[14]), np.isnan(data[13])]):
		continue

	if prevatt == -1:
		prevatt = data[13]
		prevmed = data[14]
		continue

	newx = currpos[0] + 10 * (prevatt - data[13])
	newy = currpos[1] + 10 * (prevmed - data[14])
	if newx < 0: newx = 0
	if newy < 0: newy = 0
	if newx > width: newx = width
	if newy > height: newy = height

	print((data[13], data[14]))
	print((newx,newy))
	print()

	move_mouse(newx, newy)

	currpos = [newx, newy]
	prevatt = data[13]
	prevmed = data[14]
