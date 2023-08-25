import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.io import wavfile

# fs, near_single_talk = wavfile.read('near_single_talk_44100_2_01.wav') # 音量差异不明显
# fs, near_single_talk = wavfile.read('near_single_talk_44100_2_02.wav') # 音量差异明显
# fs, near_single_talk = wavfile.read('background_noise_01.wav')
fs, near_single_talk = wavfile.read('stereo_rec_44100_2.wav')


plt.figure()
plt.subplot(311)
Pxx1, freqs1 = mlab.psd(near_single_talk[:, 0], Fs=fs, NFFT=2*fs)
plt.loglog(freqs1, Pxx1)
plt.grid('on')
plt.ylabel('PSD')
plt.xlabel('Freq (Hz)')
plt.subplot(312)
Pxx2, freqs2 = mlab.psd(near_single_talk[:, 1], Fs=fs, NFFT=2*fs)
plt.loglog(freqs2, Pxx2)
plt.grid('on')
plt.ylabel('PSD')
plt.xlabel('Freq (Hz)')
plt.subplot(313)
Pxx_diff = Pxx1 - Pxx2
# plt.loglog(freqs1, Pxx_diff)
plt.plot(freqs1, Pxx_diff)
plt.show()

