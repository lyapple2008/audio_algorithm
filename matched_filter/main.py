import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import h5py

#-------------------------------------
#-- Read in data and template
#-------------------------------------
fs = 4096
dataFile = h5py.File('data_w_signal.hdf5', 'r')
data = dataFile['strain/Strain'][...]
dataFile.close()
time = np.arange(0, 16, 1./fs)

templateFile = h5py.File('template.hdf5', 'r')
template = templateFile['strain/Strain'][...]
temp_time = np.arange(0, template.size / (1.0*fs), 1./fs)
templateFile.close()

#------------------------
# Plot data and template
#------------------------
plt.figure()
plt.plot(time,data)
plt.xlabel('Time (s)')
plt.ylabel('Strain')

plt.figure()
plt.plot(temp_time, template)
plt.xlabel('Time (s)')
plt.ylabel('Strain')
plt.title('Template')

#------------------------
# Plot ASD of data
#-----------------------
plt.figure()
power_data, freq_psd = plt.psd(data[12*fs:], Fs=fs, NFFT=fs, visible=False)
plt.close()
plt.figure()
plt.loglog(freq_psd, np.sqrt(power_data), 'b')
plt.xlim([20, 2048])
plt.xlabel('Frequency (Hz)')
plt.ylabel('ASD')
plt.grid('on')

#----------------------
# Plot ASD of template
#----------------------
power, freq = plt.psd(template, Fs=fs, NFFT=fs, visible=False)
plt.loglog(freq, np.sqrt(power), 'r')
plt.xlabel('Frequency (Hz)')
plt.ylabel('ASD')
plt.grid('on')

#-------------------------------------
# Apply a bandpass filter to the data
#------------------------------------
(B,A) = sig.butter(4, [80/(fs/2.0), 250/(fs/2.0)], btype='pass')
data_pass= sig.lfilter(B, A, data)
plt.figure()
plt.plot(time, data_pass)
plt.title('Band passed data')
plt.xlabel('Time (s)')

#------------------------------
# Time domain cross-correlation
#------------------------------
correlated_raw = np.correlate(data, template, 'valid')
correlated_passed = np.correlate(data_pass, template, 'valid')
plt.figure()
plt.plot(np.arange(0, (correlated_raw.size*1.)/fs, 1.0/fs),correlated_raw)
plt.title('Time domain cross-correlation')
plt.xlabel('Offest between data and template (s)')
plt.figure()
plt.plot(np.arange(0, (correlated_passed.size*1.)/fs, 1.0/fs), correlated_passed)
plt.xlabel('Offset between data and template (s)')
plt.title('Band passed time domain cross-correlation')

#------------------------------
# Optimal Filter, freq. domain
#------------------------------
#-- Take the FFT of the data
data_fft=np.fft.fft(data)

#--- Pad template and take FFT
zero_pad = np.zeros(data.size - template.size)
template_padded = np.append(template, zero_pad)
template_fft = np.fft.fft(template_padded)

# --- Match FFT frequency bins to PSD frequency bins
datafreq = np.fft.fftfreq(data.size)*fs
power_vec = np.interp(datafreq, freq_psd, power_data)

# --- Apply the optimal matched filter
optimal = data_fft * template_fft.conjugate() / power_vec
optimal_time = 2*np.fft.ifft(optimal)

# -- Normalize the matched filter output
df = np.abs(datafreq[1] - datafreq[0])
sigmasq = 2*(template_fft * template_fft.conjugate() / power_vec).sum() * df
sigma = np.sqrt(np.abs(sigmasq))
SNR = abs(optimal_time) / (sigma)

# -- Plot the result
plt.figure()
plt.plot(time, SNR)
plt.title('Optimal Matched Filter')
plt.xlabel('Offset time (s)')
plt.ylabel('SNR')
plt.show()