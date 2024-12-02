
import numpy as np

#stack all data in numpy arrays
from mne.io import read_raw_snirf
subject01 = read_raw_snirf("data/filtered/subject01/subject01_processed.snirf")
subject02 = read_raw_snirf("data/filtered/subject02/subject02_processed.snirf")
subject03 = read_raw_snirf("data/filtered/subject03/subject03_processed.snirf")
subject04 = read_raw_snirf("data/filtered/subject04/subject04_processed.snirf")

subject01_data = np.array(subject01.get_data())
subject02_data = np.array(subject01.get_data())
subject03_data = np.array(subject01.get_data())
subject04_data = np.array(subject01.get_data())