from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import os
import glob
#from findSN import *

current_path = os.path.dirname(os.path.abspath(__file__))
files_path = '../../N2188/Q2'
os.chdir(files_path)

name1='N2188-1.Q2.V.1610*.nh.fits'
name2='N2188-1.Q2.V.1611*.nh.fits'
name3='N2188-1.Q2.V.16120*.nh.fits'
name4='N2188-1.Q2.V.16121*.nh.fits'

files1=glob.glob(name1)
files2=glob.glob(name2)
files3=glob.glob(name3)
files4=glob.glob(name4)

files=files1+files2+files3+files4
# exclude=['N2188-1.Q2.I.161022_1635.A.028880.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161026_1624.A.029737.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161029_1606.A.030276.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161104_1549.A.031463.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161104_1658.A.031494.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161115_0036.S.041241.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161116_0132.S.041475.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161120_0033.S.042069.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161121_1609.A.034115.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161121_1724.A.034145.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161121_1726.A.034146.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161121_1730.A.034148.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161129_0238.C.039781.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161130_1401.A.035425.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161202_1707.A.035733.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161207_0236.C.041707.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161207_1557.A.036489.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161208_0345.C.041989.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161208_0454.C.042021.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161208_0709.C.042081.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161212_1558.A.037418.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161212_1658.A.037445.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161213_1551.A.037658.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161213_1705.A.037690.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161214_0047.S.045625.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161216_0050.S.046075.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161216_0153.S.046105.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161217_1620.A.038007.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161217_1728.A.038035.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161217_2345.S.046537.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161218_1305.A.038171.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161219_1622.A.038393.061035N3413.0060.nh.fits'
#          ,'N2188-1.Q2.I.161219_1726.A.038423.061035N3413.0060.nh.fits']
exclude_B=['N2188-1.Q2.B.161022_1631.A.028878.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161025_1624.A.029614.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161026_1620.A.029735.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161029_1601.A.030274.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161104_1542.A.031460.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161115_0032.S.041239.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161115_0136.S.041269.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161115_0630.C.036952.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161115_0738.C.036982.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161115_1600.A.032984.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161120_0029.S.042067.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161121_1558.A.034112.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161121_1718.A.034143.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161130_1357.A.035423.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161207_1553.A.036487.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161208_0232.C.041956.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161208_0450.C.042019.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161208_0341.C.041987.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161208_0705.C.042079.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161212_1554.A.037416.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161212_1654.A.037443.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161213_1547.A.037656.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161213_1700.A.037688.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161214_0041.S.045622.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161214_0045.S.045624.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161216_0046.S.046073.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161217_1413.A.037950.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161217_1723.A.038033.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161218_1301.A.038169.061035N3413.0060.nh.fits'
           ,'N2188-1.Q2.B.161219_1722.A.038421.061035N3413.0060.nh.fits']
exclude_V=['N2188-1.Q2.V.161022_1633.A.028879.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161022_1633.A.028879.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161029_1603.A.030275.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161115_0034.S.041240.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161115_0632.C.036953.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161115_1602.A.032985.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161119_0107.S.041887.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161120_0031.S.042068.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161121_1605.A.034114.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161130_1359.A.035424.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161201_1726.A.035675.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161202_1705.A.035732.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161207_1555.A.036488.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161207_1659.A.036515.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161208_0343.C.041988.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161208_0452.C.042020.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161208_0707.C.042080.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161212_1556.A.037417.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161212_1656.A.037444.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161213_1549.A.037657.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161213_1703.A.037689.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161216_0048.S.046074.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161216_0151.S.046104.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161217_1415.A.037951.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161217_1618.A.038006.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161217_1726.A.038034.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161217_2343.S.046536.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161218_1303.A.038170.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161219_1620.A.038392.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161219_1724.A.038422.061035N3413.0060.nh.fits'
          ,'N2188-1.Q2.V.161219_2144.S.046979.061035N3413.0060.nh.fits']           


files=set(files)-set(exclude_V)
for f in files:
    print f
    # cmd='cp '+f+' Hostgal_V/'
    # os.system(cmd)
    #findSN(f, verbosity=1, directory='/home/afsari/PycharmProjects/kspSN/corrupted/pickim/V_band/')