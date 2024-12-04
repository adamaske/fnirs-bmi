import os
import numpy as np
from mne.io import read_raw_snirf


  
subjects = ["subject01", "subject02", "subject03", "subject04"]
data = []
for subject in subjects: #load raw snirf
    path = os.path.join("data", subject, subject.join("_hb.snirf"))
    snirf = read_raw_snirf(path)
    
        
    snirf_data = np.array(snirf.get_data())
    
    # find annotaitons and start point of each task
    sfreq = snirf.info["sfreq"]
    onsets = snirf.annotations.onset
    tasks = snirf.annotations.description
    durations = snirf.annotations.duration
    labels = {"rest":0, "right" : 1, "left": 2}
    
    current_time = 0
    
    for i in range(len(onsets)):
        onset = onsets[i]
        task = tasks[i]
        label = labels[task]
        duration = durations[i]
        
        start_time = onset
        end_time = start_time + duration
        
        start_pos = int(start_time * sfreq)
        end_pos = int(end_time * sfreq)
        
        #grab everything between current_time and start_time as a "rest"
        
        current_time = end_time
        
        

    data.append(data)


