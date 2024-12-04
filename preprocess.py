import os
import numpy as np
from scipy.signal import butter, sosfiltfilt, sosfreqz

from mne.io import read_raw_snirf, RawArray
from mne_nirs.io import write_raw_snirf
from mne.preprocessing.nirs import optical_density, beer_lambert_law

from mne import create_info
from conversion import convert_all_files

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

def preprocess_all_files():

    
    filepaths = ["data/subject01/subject01_run01_hb.snirf",
             "data/subject01/subject01_run02_hb.snirf",
             "data/subject01/subject01_run03_hb.snirf",
             ]       
    for filepath in filepaths: #load hb
        hb = read_raw_snirf(filepath)   

        info = hb.info
        ch_names = info["ch_names"] 
        ch_types = info["ch_types"]
        sfreq = info["sfreq"]
        montage = hb.get_montage()
        data = np.array(hb.get_data())

        for i in range(len(data)): #filter every channel 
            data[i] = butter_bandpass_filter(data[i], 0.01, 0.08, sfreq, 10)



        raw = RawArray(data=data, info=info, verbose=True)
        raw.set_montage(montage)


        new_path = os.path.join()
        write_raw_snirf(raw, new_path)