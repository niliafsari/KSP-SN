import os
import glob
import subprocess
import commands
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from dophot import *
from findSN import *
from astropy.time import Time
from moon import *
import csv
from astropy import units as u
from astropy.coordinates import Angle

import sys
sys.path.insert(0, '/home/afsari/')

from SNAP import Astrometry



t="2017-01-20T18:50:00.000"
# loc=
#
# LATITUDE= '-32:22:42'             / Site Latitude [deg N]
# LONGITUD= '339:11:22'             / Site Longitude [deg W]
# ELEVATIO=                 1800 / Site Elevation [meters]

loc= [Angle('339:11:22 degrees').degree, Angle('-32:22:42 degrees').degree, 1800]
print Astrometry.moonLC(t, loc)

t='2017-01-20T19:58:00.000'

print Astrometry.moonLC(t, loc)