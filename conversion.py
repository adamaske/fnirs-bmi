from mne.io import read_raw_snirf
from mne_nirs.io import write_raw_snirf
from mne.preprocessing.nirs import optical_density, beer_lambert_law
import os
subjects = ["subject01", "subject02", "subject03", "subject04"]

for subject in subjects: #load raw snirf
    path = os.path.join("data", subject, subject.join(".snirf"))
    snirf = read_raw_snirf(path)

    od = optical_density(snirf)
    hb = beer_lambert_law(od)

    new_path = os.path.join("data", subject.join("_hb.snirf"))
    write_raw_snirf(hb, new_path)


