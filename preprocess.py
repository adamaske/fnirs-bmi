import os
import numpy as np
from scipy.signal import butter, sosfiltfilt, sosfreqz

from mne.io import read_raw_snirf, RawArray
from mne_nirs.io import write_raw_snirf
from mne.preprocessing.nirs import optical_density, beer_lambert_law

from mne import create_info


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

subjects = ["subject01", "subject02", "subject03", "subject04"]

for subject in subjects: #load hb
    path = os.path.join("data", subject, subject.join("_hb.snirf"))
    hb = read_raw_snirf(path)   

    info = hb.info
    ch_names = info["ch_names"] 
    ch_types = info["ch_types"]
    sfreq = info["sfreq"]
    montage = hb.get_montage()
    data = np.array(hb.get_data())

    for i in range(len(data)): #filter
        data[i] = butter_bandpass_filter(data[i], 0.01, 0.08, sfreq, 10)

    
    
    raw = RawArray(data=data, info=info, verbose=True)
    raw.set_montage(montage)

    
    new_path = os.path.join("data", subject.join("_hb.snirf"))
    write_raw_snirf(raw, new_path)


subject01_hb = read_raw_snirf("data/subject01/subject01_hb.snirf").load_data()
subject02_hb = read_raw_snirf("data/subject02/subject02_hb.snirf").load_data()
subject03_hb = read_raw_snirf("data/subject03/subject03_hb.snirf").load_data()
subject04_hb = read_raw_snirf("data/subject04/subject04_hb.snirf").load_data()

subject01_data = np.array(subject01_hb.get_data())
subject02_data = np.array(subject01_hb.get_data())
subject03_data = np.array(subject01_hb.get_data())
subject04_data = np.array(subject01_hb.get_data())
#Get Arrays
subject01_data = np.array(subject01_hb.get_data())
subject02_data = np.array(subject01_hb.get_data())
subject03_data = np.array(subject01_hb.get_data())
subject04_data = np.array(subject01_hb.get_data())


#write filtered data
#Filtering 0.01 to 0.08 Hz 
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

sampling_frequency = subject01.info["sfreq"]
filter_order = 10
lowcut = 0.01
highcut = 0.08
subject01_data = butter_bandpass_filter(subject01_data, lowcut, highcut, sampling_frequency, filter_order)
subject02_data = butter_bandpass_filter(subject02_data, lowcut, highcut, sampling_frequency, filter_order)
subject03_data = butter_bandpass_filter(subject03_data, lowcut, highcut, sampling_frequency, filter_order)
subject04_data = butter_bandpass_filter(subject04_data, lowcut, highcut, sampling_frequency, filter_order)

#Reinsert the filtered numpy arrays into the snirf objects
#TODO : How to do this?
subject01_processed = subject01_hb
subject02_processed = subject02_hb
subject03_processed = subject03_hb
subject04_processed = subject04_hb