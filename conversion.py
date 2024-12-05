from mne.io import read_raw_snirf
from mne_nirs.io import write_raw_snirf
from mne.preprocessing.nirs import optical_density, beer_lambert_law
import os

def convert_all_files():
    subject01_files = ["data/subject01/2024-12-04_001/2024-12-04_001.snirf",
                   "data/subject01/2024-12-04_002/2024-12-04_002.snirf",
                   "data/subject01/2024-12-04_003/2024-12-04_003.snirf"
                   ]
    subject02_files = ["data/subject02/2024-12-04_004/2024-12-04_004.snirf",
                       ]
    subject03_files = ["data/subject03/2024-12-04_005/2024-12-04_005.snirf",
                       ]
    subject04_files = ["data/subject04/2024-12-04_006/2024-12-04_006.snirf",
                       "data/subject04/2024-12-04_007/2024-12-04_007.snirf",
                       ]

    new_files = []

    subject_files = [subject01_files, subject02_files, subject03_files, subject04_files]
    subjects = ["subject01", "subject02", "subject03", "subject04"]
    runs = ["run01", "run02", "run03", "run04", "run05", "run06", "run07", "run08", "run09"]

    for s in range(len(subjects)):
        subject = subjects[s]
        files = subject_files[s]

        for f in range(len(files)):

            path = files[f]
            snirf = read_raw_snirf(path)

            od = optical_density(snirf)
            hb = beer_lambert_law(od)


            new_path = os.path.join("data", subject, subject + "_" + runs[f] + "_hb.snirf")
            write_raw_snirf(hb, new_path)
            new_files.append(new_path)

    return new_files

if __name__ == "__main__":
    new_files = convert_all_files()
    print("Converted to Hemoglobin : ")
    for file in new_files:
        print(file)