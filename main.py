
import os
from mne.io import read_raw_snirf
from mne_nirs.io import write_raw_snirf
from mne.preprocessing.nirs import optical_density, beer_lambert_law
import numpy as np
from scipy.signal import butter, sosfiltfilt, sosfreqz
#Adam
subject01 = read_raw_snirf("data/subject01/022_sdf_.snirf")
#Azadeh
subject02 = read_raw_snirf("data/subject02/022_sdf_.snirf")
#Daniel
subject03 = read_raw_snirf("data/subject03/022_sdf_.snirf")
#Peyman? Bindestrek? Someone?
subject04 = read_raw_snirf("data/subject04/022_sdf_.snirf")

#Raw to Optical Density
subject01_od = optical_density(subject01)
subject02_od = optical_density(subject02)
subject03_od = optical_density(subject03)
subject04_od = optical_density(subject04)
#Optical Density to Hemoglobin Concentration
subject01_hb = beer_lambert_law(subject01)
subject02_hb = beer_lambert_law(subject02)
subject03_hb = beer_lambert_law(subject03)
subject04_hb = beer_lambert_law(subject04)

#Get Arrays
subject01_data = np.array(subject01_hb.get_data())
subject02_data = np.array(subject01_hb.get_data())
subject03_data = np.array(subject01_hb.get_data())
subject04_data = np.array(subject01_hb.get_data())

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

#write filtered data
write_raw_snirf(subject01_processed, "data/filtered/subject01/subject01_processed.snirf")
write_raw_snirf(subject02_processed, "data/filtered/subject02/subject02_processed.snirf")
write_raw_snirf(subject03_processed, "data/filtered/subject03/subject03_processed.snirf")
write_raw_snirf(subject04_processed, "data/filtered/subject04/subject04_processed.snirf")