import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

ax = plt.subplot(111)

mags=np.load('test_mags.npy')
tt=np.load('tt.npy')


curve = interpolate.splrep(tt[tt > 0], mags[:, 10][tt > 0], s=0.00001)
magnew_u = interpolate.splev(tt[tt > 0], curve, der=0)

print magnew_u

plt.plot(tt, mags[:, 10])


plt.scatter(tt[tt > 0], magnew_u)
ax.invert_yaxis()
plt.show()
