import os
import numpy as np
from mne.io import read_raw_snirf
   
filepaths = ["data/subject01/subject01_run01_hb.snirf",
             "data/subject01/subject01_run02_hb.snirf",
             "data/subject01/subject01_run03_hb.snirf",
             ]       

right_data = []
left_data = []
rest_data = []
data = []
for filepath in filepaths: #load raw snirf
    snirf = read_raw_snirf(filepath)
    
        
    snirf_data = np.array(snirf.get_data())
    
    # find annotaitons and start point of each task
    sfreq = snirf.info["sfreq"]
    onsets = snirf.annotations.onset
    tasks = snirf.annotations.description
    durations = snirf.annotations.duration
    print("File : ", filepath)

    print("onsets : ", onsets)
    print("tasks : ", tasks)
    print("durations : ", durations)
    labels = {"rest":0, "right" : 1, "left": 2, "end":3}
    
    current_time = 0
    
    for i in range(len(onsets)): #for every marker
        onset = onsets[i]
        task = tasks[i]
        label = labels[task]
        duration = durations[i]
        
        if(task == 3): # skip end data
            continue

        start_time = onset #
        end_time = start_time + duration
        
        start_pos = int(start_time * sfreq) #seconds into frame
        end_pos = int(end_time * sfreq)
        
        task_data = snirf_data[:, start_pos:end_pos] #get all channels in range
        
        if label == "rest":
            rest_data.append(task_data)
        if label == "right":
            right_data.append(task_data)
        if label == "left":
            left_data.append(task_data)
    

right_data = np.array(rest_data)
left_data = np.array(right_data)
rest_data = np.array(left_data)