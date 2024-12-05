import os
import numpy as np
from mne.io import read_raw_snirf
from preprocess import preprocess_data
filepaths = [  "data\subject01\subject01_run01_hb.snirf",
               "data\subject01\subject01_run02_hb.snirf",
               "data\subject01\subject01_run03_hb.snirf",
               "data\subject02\subject02_run01_hb.snirf",
               "data\subject03\subject03_run01_hb.snirf",
               "data\subject04\subject04_run01_hb.snirf",
               "data\subject04\subject04_run02_hb.snirf",
             ]       

rest_epochs = []
right_epochs = []
left_epochs= []

for filepath in filepaths: #load raw snirf
    snirf = read_raw_snirf(filepath)
    snirf_data = np.array(snirf.get_data())
    sfreq = snirf.info["sfreq"]
    pre_procssed_data = preprocess_data(snirf_data, 0.01, 0.08, sfreq, 10)
    
    onsets = snirf.annotations.onset[:-2]
    tasks = snirf.annotations.description[:-2]
    durations = snirf.annotations.duration[:-2]
    print("snirf : ", filepath)
    print("onsets : ", onsets)
    print("tasks : ", tasks)
    print("durations : ", durations)
    labels = {0:"rest", 1:"right", 2:"left", 3:"end"}
    class_durations = {"rest":20, "right":10, "left":10, "end":0}
    for i in range(len(onsets)): #for every marker
        onset = onsets[i]
        task = tasks[i]
        label = labels[int(task)]
        duration = class_durations[label]

        if label == "end":
            print("end_label found")
            continue
        
        start_time = onset #
        end_time = start_time + duration
        
        if label == "rest": # extract seconds 5 to 15 from the rest
            start_time = onset + (duration / 4)
            end_time = start_time + (duration / 2)
                
        start_pos = int(start_time * sfreq) #seconds into frame
        end_pos = int(end_time * sfreq)
        
        task_data = pre_procssed_data[:, start_pos:end_pos] #get all channels in range
        cropped_data = task_data[:, :50]
        
        if label == "rest":
            rest_epochs.append(cropped_data)
        if label == "right":
            right_epochs.append(cropped_data)
        if label == "left":
            left_epochs.append(cropped_data)
    
print("rest epochs : ", len(rest_epochs))
print("right epochs : ", len(right_epochs))
print("left epochs : ", len(left_epochs))

rest_data = np.array(rest_epochs)
right_data = np.array(right_epochs)
left_data = np.array(left_epochs)
np.save("data/rest_epochs.np", rest_data)
np.save("data/right_epochs.np", right_data)
np.save("data/left_epochs.np", left_data)
print("saved rest_epochs : ", rest_data.shape, ":  data/rest_epochs.np")
print("saved right_ecpohs : ", right_data.shape, ":  data/right_epochs.np")
print("saved left_epochs : ", left_data.shape, ":  data/left_epochs.np")