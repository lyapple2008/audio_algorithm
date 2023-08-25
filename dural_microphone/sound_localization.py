import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.io import wavfile
from scipy import signal

# rng = np.random.default_rng()
# x = np.arange(128) / 128
# sig = np.sin(2 * np.pi * x)
# sig_noise = sig + rng.standard_normal(len(sig))
# corr = signal.correlate(sig_noise, sig)
# lags = signal.correlation_lags(len(sig), len(sig_noise))
# corr /= np.max(corr)

# fs, near_single_talk = wavfile.read('near_single_talk_44100_2_01.wav') # 音量差异不明显
# fs, near_single_talk = wavfile.read('near_single_talk_44100_2_02.wav') # 音量差异明显
fs, near_single_talk = wavfile.read('background_noise_01.wav')

len = 512
start = 1024
end = start + len
corr = signal.correlate(near_single_talk[start:end, 0].astype(np.float64), near_single_talk[start:end, 1].astype(np.float64))
lags = signal.correlation_lags(len, len)
# corr /= np.max(corr)
lag = lags[np.argmax(corr)]
print("lag: %d" % lag)


plt.figure()
plt.subplot(311)
plt.plot(near_single_talk[start+lag:end+lag, 0])
plt.subplot(312)
plt.plot(near_single_talk[start:end, 1])
plt.subplot(313)
# plt.plot(lags, corr)
plt.plot(np.abs(near_single_talk[start+lag:end+lag, 0] - near_single_talk[start:end, 1]))
plt.show()
