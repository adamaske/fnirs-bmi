import os
import numpy as np
from scipy.signal import butter, sosfiltfilt, sosfreqz
from scipy.stats import zscore

def butter_bandpass(lowcut, highcut, fs, freqs=512, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], btype='band', output='sos')
    w, h = sosfreqz(sos, worN=2000, whole=True, fs=fs)
    return sos, w, h

def butter_bandpass_filter(time_series, lowcut, highcut, fs, order):
    sos, w, h = butter_bandpass(lowcut, highcut, fs, order=order)
    y = sosfiltfilt(sos, time_series)
    return y

def preprocess_data(data, lowcout, highcut, fs, order):
    filtered = data
    for i in range(len(filtered)): #each cahnnel
        filtered[i] = butter_bandpass_filter(filtered[i], lowcout, highcut, fs, order)
        
    #z - normalize
    noramlized = zscore(filtered, axis=None)
    return noramlized
