import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#%% Get the UTC time difference in hours
timezone = 2

#%% lat and lon of bern
lat = 46.9480896
lon = 7.4474401

#%% Get the local time
date = '2020-01-14'
localtime = pd.date_range(date, periods=24*60, freq='T')
    
#%% Get the day of the year and others
DoY = [ localtime[p].timetuple().tm_yday for p in range(0, len(localtime))]
hour = [localtime[p].hour for p in range(0, len(localtime))]
minute = [localtime[p].minute for p in range(0, len(localtime))]
second = [localtime[p].second for p in range(0, len(localtime))]

# Get the fractional year
gamma = [(2 * np.pi / 365) * (DoY[p] - 1 + ((hour[p] -12) / 24)) \
         for p in range(0, len(DoY))]

# Get declination
decl = [0.006918 - 0.399912 * np.cos(gamma[p]) + 0.070257 * np.sin(gamma[p]) \
        - 0.006758 * np.cos(2 * gamma[p]) + 0.000907 * np.sin(2 * gamma[p]) \
        - 0.002697 * np.cos(3 * gamma[p]) + 0.00148 * np.sin(3 * gamma[p]) \
        for p in range(0, len(gamma))]

# Equation of time
eqtime = [229.18 * (0.000075 + 0.001868 * np.cos(gamma[p]) - 0.032077 * \
        np.sin(gamma[p]) - 0.014615 * np.cos(2 * gamma[p]) - \
        0.040849 * np.sin(2 * gamma[p])) for p in range(0, len(gamma))]

# Get time offset
time_offset = [eqtime[p] + 4 * lon \
               - 60 * timezone for p in range(0, len(eqtime))]

# ??
tst = [hour[p] * 60 + minute[p] + second[p] / 60 + time_offset[p] for p in range(0,len(hour))]

# Get the solar hour angle
ha = [(tst[p] / 4) - 180 for p in range(0,len(tst))]

# Degrees to rad
deg_to_rad = 2 * np.pi / 360

#%% Get the solar zenith angle
sza = [np.arccos(np.sin(lat *deg_to_rad) \
        * np.sin(decl[p]) + np.cos(lat*deg_to_rad) \
        * np.cos(decl[p]) * np.cos(ha[p]*deg_to_rad)) for p in range(0,len(decl))]

# Get the solar azimuth
saz = [(np.arccos(-(np.sin(lat *deg_to_rad)\
        * np.cos(sza[p]) - np.sin(decl[p]))/(np.cos(lat *deg_to_rad) \
        * np.sin(sza[p]))) * (-1) - 180) * deg_to_rad for p in range(0,len(sza))] 

#%% Get air mass
am = []
for q in range(0, len(sza)):
    if sza[q] > np.pi/2:
        am.append(float('nan'))
    else:
        am.append(1/np.cos(sza[q]))

        

maxamind = am.index(np.nanmin(am))
print(localtime[maxamind])

plt.figure()
plt.plot(localtime, am)
plt.plot([localtime[0], localtime[-1]], [1.5, 1.5])
plt.xlabel('datetime')
plt.ylabel('AM')
plt.title('Bern, Switzerland, ' + date)
plt.gca().invert_yaxis()
plt.ylim([4,1])
plt.xlim([localtime[0], localtime[-1]])

myFmt = mdates.DateFormatter('%H:%M') # here you can format your datetick labels as desired
plt.gca().xaxis.set_major_formatter(myFmt)
plt.show()