# Arrays and handling data
#import numpy as np
#import pandas as pd

#from astropy.io import fits # Astronomical files

# Plotting data
import matplotlib
from matplotlib import pyplot as plot
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Accessing local files
#import os 
#import sys
import pickle

#from astropy.wcs import WCS # Converting between pixels and WCS

#import json


#cone = []
#with open("cone.txt", "r") as file:
#    json_file = json.loads(file.read().replace("'", "\"").replace("None", "\"None\""))
#    cone = pd.DataFrame(json_file["data"])

#print(len(cone))

all_star_data = []
with open("FINAL_0-299.pkl", "rb") as file:
    loaded_dict = pickle.load(file)
    print(len(loaded_dict))
    print(len(loaded_dict["Target"]["brightness"]))
    print(loaded_dict.keys())
    all_star_data = loaded_dict


#for i in all_star_data.keys():
#    #print(str(i) + "   " + str(len(all_star_data[str(i)]["time"])))

period = 0.3681414
plot_times = []
plot_times_phase_folded = []
plot_brightnesses = []
plot_103_brightnesses = []
plot_614_brightnesses = []
here_count = 0
skip_count = 0 # 614 and 103 are longest
individual_star_index = 225
for time_index in range(len(all_star_data["Target"]["time"])):
    here_count += 1
    #if all_star_data["Target"]["time"][time_index] in all_star_data[str(individual_star_index)]["time"]:
    if (all_star_data["Target"]["time"][time_index] in all_star_data[str(individual_star_index)]["time"]) and (all_star_data["Target"]["time"][time_index] in all_star_data[str(103)]["time"]):
        test_index_614 = all_star_data[str(individual_star_index)]["time"].index(all_star_data["Target"]["time"][time_index])
        test_index_103 = all_star_data[str(103)]["time"].index(all_star_data["Target"]["time"][time_index])
        plot_times_phase_folded.append(all_star_data["Target"]["time"][time_index] % period)
        plot_times.append(all_star_data["Target"]["time"][time_index])
        #plot_brightnesses.append((all_star_data["Target"]["brightness"][time_index]) / (all_star_data[str(individual_star_index)]["brightness"][test_index]))
        plot_brightnesses.append((all_star_data["Target"]["brightness"][time_index]) / (all_star_data[str(individual_star_index)]["brightness"][test_index_614] + all_star_data[str(103)]["brightness"][test_index_103]))
        
        #if all_star_data["filter blah
        plot_103_brightnesses.append(all_star_data[str(103)]["brightness"][test_index_103])
        plot_614_brightnesses.append(all_star_data[str(individual_star_index)]["brightness"][test_index_614])
    else:
        print("ERROR: " + str(all_star_data["Target"]["time"][time_index]))
        skip_count += 1
    
    #if all_star_data[str(103)]["time"][time_index] in all_star_data[str(individual_star_index)]["time"]:
    #    test_index_614 = all_star_data[str(individual_star_index)]["time"].index(all_star_data["Target"]["time"][time_index])
    #    test_index_103 = all_star_data[str(103)]["time"].index(all_star_data["Target"]["time"][time_index])
    #    plot_103_brightnesses.append(all_star_data[str(103)]["brightness"][test_index_103])
    #    plot_614_brightnesses.append(all_star_data[str(individual_star_index)]["brightness"][test_index_614])

print("Here count: " + str(here_count))
print("Skip count: " + str(skip_count))
figure, ax = plot.subplots()
ax.plot(plot_103_brightnesses, plot_614_brightnesses, ".")
ax.set_yscale("log")
#ax.set_ylabel("
ax.set_xscale("log")
plot.show()


figure, ax = plot.subplots()
ax.plot(plot_times, plot_brightnesses, ".")
#ax.plot(plot_times_phase_folded, plot_brightnesses, ".")
ax.set_yscale("log")
plot.show()
figure, ax = plot.subplots()
#ax.plot(plot_times, plot_brightnesses, ".")
ax.plot(plot_times_phase_folded, plot_brightnesses, ".")
ax.set_yscale("log")
plot.show()