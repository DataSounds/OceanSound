#/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Ler e agrupar os hdfs,
para aplicar a EOF
'''

from pyhdf.SD import *
import numpy as np
import glob
#from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


LATLIMS=([-90, 90])
LONLIMS=([-180, 179.99])

indir = '/home/wuah/Imagens/MODIS/'

filelist = glob.glob(indir+'A*')
nfiles = len(filelist)
files = []
for path in filelist:
  files.append(path[len(indir):]) #remove path name

A = SD(filelist[0])
a = A.attributes()

names=[]
for k in xrange(0,len(a.keys())):
    nm = a.keys()[k]
    names.append(nm.replace(" ","_"))

pin  = dict(zip(names,a.values()[:]))
lon = np.arange(pin['Westernmost_Longitude'],pin['Easternmost_Longitude'],pin['Longitude_Step'])
lat= np.arange(pin['Northernmost_Latitude'],pin['Southernmost_Latitude'],-pin['Latitude_Step'])

#Get the indices needed for the area of interest
ilt = np.int(np.argmin(np.abs(lat-max(LATLIMS)))) #argmin catch the indices
ilg = np.int(np.argmin(np.abs(lon-min(LONLIMS)))) #of minor element
ltlm = np.int(np.fix(np.diff(LATLIMS)/pin['Latitude_Step']+0.5))
lglm = np.int(np.fix(np.diff(LONLIMS)/pin['Longitude_Step']+0.5))

#retrieve data SDS
d = A.datasets()
sds_name = d.keys()[0] #pegar o nome do sds. Método de dictionary.
sds = A.select(sds_name)
#load the subset of data needed for the map limits given
#P = sds[ilt:(ilt+ltlm),ilg:(ilg+lglm)]
#P[P==-32767]=np.nan #Rrs_670:bad_value_scaled = -32767s ;
#P=np.double(P)
#P=(pin['Slope']*P+pin['Intercept'])
LT=lat[ilt+np.arange(0,ltlm)]
LG=lon[ilg+np.arange(0,lglm)]
Plg,Plt = np.meshgrid(LG,LT)

#Combining images
data = np.zeros([len(filelist),ltlm,lglm])
#for i in range(len(filelist)):
for i in range(1):
    A = SD(filelist[i])
    d = A.datasets()
    sds_name = d.keys()[0]
    sds = A.select(sds_name)
    data[i] = sds.get()

data = np.ma.masked_values(data,-32767)
data = (pin['Slope']*data+pin['Intercept'])
data = np.log(data)

np.save('multi_data',data)

