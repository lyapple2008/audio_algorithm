import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.io import wavfile
from scipy import signal

# fs, far_single_talk = wavfile.read('far_single_talk_44100_1.wav')
fs, far_single_talk = wavfile.read('stereo_rec_44100_2.wav')


# plt.figure()
# plt.subplot(311)
# Pxx1, freqs1 = mlab.psd(far_single_talk[:, 0], Fs=fs, NFFT=2*fs)
# plt.loglog(freqs1, Pxx1)
# plt.grid('on')
# plt.ylabel('PSD')
# plt.xlabel('Freq (Hz)')
# plt.subplot(312)
# Pxx2, freqs2 = mlab.psd(far_single_talk[:, 1], Fs=fs, NFFT=2*fs)
# plt.loglog(freqs2, Pxx2)
# plt.grid('on')
# plt.ylabel('PSD')
# plt.xlabel('Freq (Hz)')
# plt.subplot(313)
# Pxx_diff = Pxx1 - Pxx2
# plt.loglog(freqs1, Pxx_diff)
# # plt.plot(freqs1, Pxx_diff)
# plt.show()

len = far_single_talk[:,0].size
start = 0
end = start + len
print(end)
corr = signal.correlate(far_single_talk[start:end, 0].astype(np.float64), far_single_talk[start:end, 1].astype(np.float64))
lags = signal.correlation_lags(len, len)
# corr /= np.max(corr)
lag = lags[np.argmax(corr)]
print("lag: %d" % lag)


plt.figure()
plt.subplot(311)
plt.plot(far_single_talk[start+lag:end+lag, 0])
plt.subplot(312)
plt.plot(far_single_talk[start:end, 1])
plt.subplot(313)
# plt.plot(lags, corr)
plt.plot(np.abs(far_single_talk[start+lag:end, 0] - far_single_talk[start:end-lag, 1]))
plt.show()