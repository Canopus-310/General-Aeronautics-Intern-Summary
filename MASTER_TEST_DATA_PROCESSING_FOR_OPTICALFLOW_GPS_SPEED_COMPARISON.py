from pymavlink import mavutil
import os
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict
import shutil

bin_folder = Path(r"C:\Users\GA\Desktop\binfiles")
csv_folder = bin_folder / "converted"
# remove the existing files inside csv folder to remove stale and old csv files and start fresh - why? if you might need to remove the newly added files to compare the newest median error with the previous median error
if csv_folder.exists():
    shutil.rmtree(csv_folder)
csv_folder.mkdir(exist_ok=True) # exist ok = create the folder but dont crash if it already exists


for bin_file in sorted(bin_folder.glob("*.bin")):
    number = bin_file.stem  # "278", "279" etc.
    
    log = mavutil.mavlink_connection(str(bin_file)) # opens the bin file and prepares it for message-by-message reading

    gps_rows = []
    of_rows = []

    while True: 
        msg = log.recv_match(type=["GPS", "OF"]) # fetches the next message that is either GPS or OF type — returns None when log is exhausted
        if msg is None:
            break   
        d = msg.to_dict() # converts that single message into a flat dictionary of its fields e.g. {"TimeUS": 123, "Speed": 1.2 ...}
        if msg.get_type() == "GPS":
            gps_rows.append(d)
        else:
            of_rows.append(d)
    
    pd.DataFrame(gps_rows).to_csv(csv_folder / f"{number} - GPS.csv")
    pd.DataFrame(of_rows).to_csv(csv_folder / f"{number} - OF.csv")
    

# Find all CSV files
folder = csv_folder
groups = defaultdict(dict)

height = 1.2 #METRES
OUTLIER_THRESHOLD = 50 # percent
error_list = []

for f in sorted(folder.glob("*.csv")):
    number, tag = f.stem.split(" - ")
    groups[number][tag] = f

for number, files in groups.items():
    loaded = {} # fresh new dictionary
    for tag, path in files.items(): # tag is gps or of and path is their location in computer
        loaded[f"{number}_{tag}"] = pd.read_csv(path)

    df_gps = loaded[f"{number}_GPS"]
    df_of = loaded[f"{number}_OF"]

    GPS_speed = df_gps['Spd'].median()

    df_of["OF_speed"] = height * np.sqrt((df_of["bodyX"]- df_of['flowX'])**2 + (df_of["bodyY"]-df_of["flowY"])**2)
    OF_speed = df_of["OF_speed"].median()

    
    error = abs(OF_speed - GPS_speed) / abs(GPS_speed) * 100

    print(f"From bin number {number} data:")
    print(f"GPS median speed: {GPS_speed: .4f}")
    print(f"OF speed detected: {OF_speed: .4f}")
    print(f"Error margin for this data set: {error: .4f} ")
    print()

    if error > OUTLIER_THRESHOLD: #this is to avoid skewing the average and median error from unusual high error situations
        print(f" ⚠ Bin {number} excluded — error {error:.1f}% exceeds threshold")
        print()
        continue  # skip appending to error_list # continue - it exits the current iteration of the entire loop and moves to the next number itself
    
    error_list.append(error)

#median error calculate here
median_error = np.median(error_list)
average_error = np.average(error_list)
print(f"The median error from all of the above data is {median_error: .4f}")
print(f"The average error from all of the above data is {average_error: .4f}")
print()
