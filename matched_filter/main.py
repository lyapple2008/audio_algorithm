# -- Import python data and plotting packages 
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import h5py

# -- Read the data file (16 seconds, sampled at 4096 Hz)
fs = 4096
dataFile = h5py.File('data_w_signal.hdf5', 'r')
data = dataFile['strain/Strain'][...]
dataFile.close()
time = np.arange(0, 16, 1./fs)

# -- Read the template file (1 second, sampled at 4096 Hz)
templateFile = h5py.File('template.hdf5', 'r')
template = templateFile['strain/Strain'][...]
temp_time = np.arange(0, template.size / (1.0*fs), 1./fs)
templateFile.close()