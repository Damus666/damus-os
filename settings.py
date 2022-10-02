from screeninfo import get_monitors
import json_helper
#from pygame_helper.helper import medium_calculator

for m in get_monitors():
    SIZES = (m.width,m.height)
    
obj = json_helper.Json.LoadObject("data/programsdata/Settings.json")
res = obj.GetValue("resolution",False).value

if res != "Fullscreen":
    w,h = res.split("x")
    SIZES = (int(w),int(h))

W = SIZES[0]
H = SIZES[1]

MW = 1920
MH = 1080

def width_calculator(desired_result,rounded:bool=False):
	divider = MW/desired_result
	pixels = W/divider
	if rounded:
		return round(pixels)
	else:
		return pixels

def height_calculator(desired_result,rounded:bool=False):
	divider = MH/desired_result
	pixels = H/divider
	if rounded:
		return round(pixels)
	else:
		return pixels

def medium_calculator(desired_result,rounded:bool=False):
	first = width_calculator(desired_result,rounded)
	second = height_calculator(desired_result,rounded)
	pixels = (first+second)/2
	if rounded:
		return round(pixels)
	else:
		return pixels

# elements
BARH = 40
PINPUTW = 250
BARBW = 200
BUTTONW = 150
BUTTONH = 40
CBH = 40
CBW = 70

# paths
DATAF = "data/"
IMAGESF = DATAF+"images/files/"
PROGRAMSF = DATAF+"programsdata/"

# user
USERPFPSIZES = (150,150)