# Arrays and handling data
import numpy as np
import pandas as pd

# Plotting data
import matplotlib
from matplotlib import pyplot as plot
from mpl_toolkits.axes_grid1 import make_axes_locatable # Color log
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes # Zoom
from mpl_toolkits.axes_grid1.inset_locator import mark_inset # Zoom 

import math



# Stuff from TOI Catalog
tic_ID = "TIC 155657581" # SIMBAD4 flickers really brightly so it should be easy to spot
period = 0.3681414 # days
transit_depth = 0.5 / 17.1384 * 1000000 # ppm so actual is 0.5
mean_g_filter_magnitude = 15
mean_r_filter_magnitude = 15
mean_i_filter_magnitude = 15
name = "SIMBAD4_mdwarf"

tic_ID = "TIC 230075121"
period = 0.7676704 # days
transit_depth = 330 # ppm
tess_magnitude = 17.1384
mean_g_filter_magnitude = 20.06909942626953 # gMeanPSFMag
mean_r_filter_magnitude = 18.93829917907715 # rMeanPSFMag
mean_i_filter_magnitude = 17.68600082397461 # iMeanPSFMag
name = "230075121"




transit_depth = transit_depth / 1000000 * tess_magnitude
print(transit_depth)
all_star_dataframe = pd.read_csv("All_" + name + "_Star_Data.csv") #All_Star_Data_3 #All_MYSTERY_TOI_Star_Data #All_SIMBAD4_MDWARF_Star_Data
cone = pd.read_csv(name + "_Cone.csv") # All_Star_Data_3_Cone

delta_m = np.log(1 / transit_depth) / np.log(2.512) # Positive number

usable_dataframe = all_star_dataframe[["time", "image_filter"]].copy()
for column in all_star_dataframe.columns[9::3]:
    if all_star_dataframe[column].isnull().sum() < (len(all_star_dataframe[column]) / 2): # If more than half the number of frames have calculated brightness values
        if cone.at[int(np.where(cone["ID"] == int(column.split("_")[0]))[0]), "Tmag"] < (cone.at[int(np.where(cone["ID"] == int(tic_ID.split()[1]))[0]), "Tmag"] + delta_m): # Bright enough to effect signal
            print(max(list(all_star_dataframe[column])))
            if max(list(all_star_dataframe[column])) < 55000: # Making sure it is not saturated
                if (cone.at[int(np.where(cone["ID"] == int(column.split("_")[0]))[0]), "Tmag"] > 13) and cone.at[int(np.where(cone["ID"] == int(column.split("_")[0]))[0]), "Tmag"] < 20:
                    usable_dataframe[column] = all_star_dataframe[column]
        
usable_dataframe[str(tic_ID.split()[1]) + "_brightness"] = all_star_dataframe[str(tic_ID.split()[1]) + "_brightness"]
print(str(len(usable_dataframe.columns) - 2) + " stars are usable out of " + str(len(all_star_dataframe.columns[9::3])))
comparison_dataframe = usable_dataframe
#comparison_dataframe = all_star_dataframe[["time", "image_filter", "155657569_brightness", "155657576_brightness", (str(tic_ID.split()[1]) + "_brightness"), "1001612129_brightness" , "155656195_brightness"]].copy()
################comparison_dataframe = all_star_dataframe[["time", "image_filter", "230076800_brightness", "230076814_brightness", (str(tic_ID.split()[1]) + "_brightness")]].copy() # "230075120_brightness",
#comparison_dataframe = all_star_dataframe[["time", "image_filter", "230075122_brightness", "230075123_brightness", "230076807_brightness", "230076797_brightness", "230076815_brightness", (str(tic_ID.split()[1]) + "_brightness")]].copy()
#comparison_dataframe = all_star_dataframe[["time", "image_filter", "230076815_brightness", "230076797_brightness", (str(tic_ID.split()[1]) + "_brightness")]].copy()

#plot.plot(comparison_dataframe["230076815_brightness"], comparison_dataframe["230076797_brightness"], ".")
#plot.show() # 230076800_brightness, 230076814_brightness

# Clearing the nan rows so all of the rows have data
for column_name in comparison_dataframe.columns[2:]:
    comparison_dataframe = comparison_dataframe[comparison_dataframe[column_name].notnull()]
#print(comparison_dataframe.isnull().values.any()) # Should be False because all nans have been moved
#print(comparison_dataframe)

ZTF_g_dataframe = comparison_dataframe[(comparison_dataframe["image_filter"] == "ZTF_g") | (comparison_dataframe["image_filter"] == "ZTF g")]
ZTF_r_dataframe = comparison_dataframe[(comparison_dataframe["image_filter"] == "ZTF_r") | (comparison_dataframe["image_filter"] == "ZTF r")]
ZTF_i_dataframe = comparison_dataframe[(comparison_dataframe["image_filter"] == "ZTF_i") | (comparison_dataframe["image_filter"] == "ZTF i")]

target_star_header_index = list(comparison_dataframe.columns).index(str(tic_ID.split()[1]) + "_brightness") - 2 # Need to exclude this column from the comparisons
#target_star_header_index = list(comparison_dataframe.columns).index("230075121_brightness") - 2
print(target_star_header_index)


def factor_int(n):
    val = math.ceil(math.sqrt(n))
    val2 = int(n/val)
    while val2 * val != float(n):
        val -= 1
        val2 = int(n/val)
    return max(val, val2), min(val, val2)

plot_y_grid, plot_x_grid = factor_int(len(comparison_dataframe.columns) - 2)


# Plotting
def get_comparison_sums(dataframe_column, ics):
    sum = 0
    for i in ics: sum += np.array(dataframe_column[i])
    return sum


column_index = 0
if plot_x_grid == 1:
    figure, ax = plot.subplots(plot_y_grid, sharex = True, sharey = True)
    figure.subplots_adjust(bottom = 0.05, top = 0.975, left = 0.05, right = 0.975, wspace = 0.05, hspace = 0.35)
    
    ax[0].set_xlim([0, period])
    #ax[0].set_ylim([1 - transit_depth - 0.05, 1 + (transit_depth / 10)])
    ax[0].set_ylim([0.75, 1.25])
    
    for y_ax in range(plot_y_grid):
        ax[y_ax].set_xlabel("TIC " + str((list(comparison_dataframe.columns[2:])[column_index]).split("_")[0]))
        ax[y_ax].xaxis.set_label_position("top")
        
        immediate_comparison_stars = list(comparison_dataframe.columns[2:])
        del immediate_comparison_stars[column_index]
        column_name = str((list(comparison_dataframe.columns[2:])[column_index]))
        
        if column_index == target_star_header_index:
            if not ZTF_g_dataframe.empty and (mean_g_filter_magnitude < 17.75):
               ax[column_index].plot((np.array(ZTF_g_dataframe["time"]) % period), (np.array(ZTF_g_dataframe[column_name]) / get_comparison_sums(ZTF_g_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_g_dataframe[column_name]) / get_comparison_sums(ZTF_g_dataframe, immediate_comparison_stars))), ".", color = "b", alpha = 0.3)
            if not ZTF_r_dataframe.empty and (mean_r_filter_magnitude < 17.75):
                ax[column_index].plot((np.array(ZTF_r_dataframe["time"]) % period), (np.array(ZTF_r_dataframe[column_name]) / get_comparison_sums(ZTF_r_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_r_dataframe[column_name]) / get_comparison_sums(ZTF_r_dataframe, immediate_comparison_stars))), ".", color = "r", alpha = 0.3)
            if not ZTF_i_dataframe.empty and (mean_i_filter_magnitude < 17.75):
                ax[column_index].plot((np.array(ZTF_i_dataframe["time"]) % period), (np.array(ZTF_i_dataframe[column_name]) / get_comparison_sums(ZTF_i_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_i_dataframe[column_name]) / get_comparison_sums(ZTF_i_dataframe, immediate_comparison_stars))), ".", color = "brown", alpha = 0.3)
        else:
            immediate_comparison_stars.remove(list(comparison_dataframe.columns[2:])[target_star_header_index]) # We don't want this signal to interfere with our data
            
            if not ZTF_g_dataframe.empty:
                ax[column_index].plot((np.array(ZTF_g_dataframe["time"]) % period), (np.array(ZTF_g_dataframe[column_name]) / get_comparison_sums(ZTF_g_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_g_dataframe[column_name]) / get_comparison_sums(ZTF_g_dataframe, immediate_comparison_stars))), ".", color = "b", alpha = 0.3)
            if not ZTF_r_dataframe.empty:
                ax[column_index].plot((np.array(ZTF_r_dataframe["time"]) % period), (np.array(ZTF_r_dataframe[column_name]) / get_comparison_sums(ZTF_r_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_r_dataframe[column_name]) / get_comparison_sums(ZTF_r_dataframe, immediate_comparison_stars))), ".", color = "r", alpha = 0.3)
            if not ZTF_i_dataframe.empty:
                ax[column_index].plot((np.array(ZTF_i_dataframe["time"]) % period), (np.array(ZTF_i_dataframe[column_name]) / get_comparison_sums(ZTF_i_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_i_dataframe[column_name]) / get_comparison_sums(ZTF_i_dataframe, immediate_comparison_stars))), ".", color = "brown", alpha = 0.3)
        
        column_index += 1
else:
    figure, ax = plot.subplots(plot_y_grid, plot_x_grid, sharex = True, sharey = True)
    figure.subplots_adjust(bottom = 0.05, top = 0.975, left = 0.05, right = 0.975, wspace = 0.05, hspace = 0.35)
    
    ax[0, 0].set_xlim([0, period])
    #ax[0, 0].set_ylim([1 - transit_depth - 0.05, 1 + (transit_depth / 10)])
    ax[0, 0].set_ylim([(1 - (transit_depth * 2)), (1 + (transit_depth * 2))])
    #ax[0, 0].set_ylim([0.75, 1.25])
    
    for y_ax in range(plot_y_grid): 
        for x_ax in range(plot_x_grid):
            ax[y_ax, x_ax].set_xlabel("TIC " + str((list(comparison_dataframe.columns[2:])[column_index]).split("_")[0]))
            ax[y_ax, x_ax].xaxis.set_label_position("top")
            
            immediate_comparison_stars = list(comparison_dataframe.columns[2:])
            del immediate_comparison_stars[column_index]
            column_name = str((list(comparison_dataframe.columns[2:])[column_index]))
            
            if column_index == target_star_header_index:
                if not ZTF_g_dataframe.empty and (mean_g_filter_magnitude < 17.75):
                   ax[y_ax, x_ax].plot((np.array(ZTF_g_dataframe["time"]) % period), (np.array(ZTF_g_dataframe[column_name]) / get_comparison_sums(ZTF_g_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_g_dataframe[column_name]) / get_comparison_sums(ZTF_g_dataframe, immediate_comparison_stars))), ".", color = "b", alpha = 0.3)
                if not ZTF_r_dataframe.empty and (mean_r_filter_magnitude < 17.75):
                    ax[y_ax, x_ax].plot((np.array(ZTF_r_dataframe["time"]) % period), (np.array(ZTF_r_dataframe[column_name]) / get_comparison_sums(ZTF_r_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_r_dataframe[column_name]) / get_comparison_sums(ZTF_r_dataframe, immediate_comparison_stars))), ".", color = "r", alpha = 0.3)
                if not ZTF_i_dataframe.empty and (mean_i_filter_magnitude < 17.75):
                    ax[y_ax, x_ax].plot((np.array(ZTF_i_dataframe["time"]) % period), (np.array(ZTF_i_dataframe[column_name]) / get_comparison_sums(ZTF_i_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_i_dataframe[column_name]) / get_comparison_sums(ZTF_i_dataframe, immediate_comparison_stars))), ".", color = "brown", alpha = 0.3)
            else:
                immediate_comparison_stars.remove(list(comparison_dataframe.columns[2:])[target_star_header_index]) # We don't want this signal to interfere with our data
                
                if not ZTF_g_dataframe.empty:
                    ax[y_ax, x_ax].plot((np.array(ZTF_g_dataframe["time"]) % period), (np.array(ZTF_g_dataframe[column_name]) / get_comparison_sums(ZTF_g_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_g_dataframe[column_name]) / get_comparison_sums(ZTF_g_dataframe, immediate_comparison_stars))), ".", color = "b", alpha = 0.3)
                if not ZTF_r_dataframe.empty:
                    ax[y_ax, x_ax].plot((np.array(ZTF_r_dataframe["time"]) % period), (np.array(ZTF_r_dataframe[column_name]) / get_comparison_sums(ZTF_r_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_r_dataframe[column_name]) / get_comparison_sums(ZTF_r_dataframe, immediate_comparison_stars))), ".", color = "r", alpha = 0.3)
                if not ZTF_i_dataframe.empty:
                    ax[y_ax, x_ax].plot((np.array(ZTF_i_dataframe["time"]) % period), (np.array(ZTF_i_dataframe[column_name]) / get_comparison_sums(ZTF_i_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_i_dataframe[column_name]) / get_comparison_sums(ZTF_i_dataframe, immediate_comparison_stars))), ".", color = "brown", alpha = 0.3)
            
            column_index += 1
'''
figure, ax = plot.subplots(len(comparison_dataframe.columns) - 2, sharex = True)
for column_name in comparison_dataframe.columns[2 : end_index + 2]:
    immediate_comparison_stars = list(comparison_dataframe.columns[2:])
    del immediate_comparison_stars[column_index]
    
    ax[column_index].set_title("TIC " + str(column_name.split("_")[0]))
    ax[column_index].set_xlim([0, period])
    #ax[column_index].set_ylim([0.75, 1.25])
    ax[column_index].set_ylim([transit_depth, 1.05])
    
    if column_index == target_star_header_index:
        if not ZTF_g_dataframe.empty and (mean_g_filter_magnitude < 17.75):
           ax[column_index].plot((np.array(ZTF_g_dataframe["time"]) % period), (np.array(ZTF_g_dataframe[column_name]) / get_comparison_sums(ZTF_g_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_g_dataframe[column_name]) / get_comparison_sums(ZTF_g_dataframe, immediate_comparison_stars))), ".", color = "b", alpha = 0.3)
        if not ZTF_r_dataframe.empty and (mean_r_filter_magnitude < 17.75):
            ax[column_index].plot((np.array(ZTF_r_dataframe["time"]) % period), (np.array(ZTF_r_dataframe[column_name]) / get_comparison_sums(ZTF_r_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_r_dataframe[column_name]) / get_comparison_sums(ZTF_r_dataframe, immediate_comparison_stars))), ".", color = "r", alpha = 0.3)
        if not ZTF_i_dataframe.empty and (mean_i_filter_magnitude < 17.75):
            ax[column_index].plot((np.array(ZTF_i_dataframe["time"]) % period), (np.array(ZTF_i_dataframe[column_name]) / get_comparison_sums(ZTF_i_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_i_dataframe[column_name]) / get_comparison_sums(ZTF_i_dataframe, immediate_comparison_stars))), ".", color = "brown", alpha = 0.3)
    else:
        immediate_comparison_stars.remove(list(comparison_dataframe.columns[2:])[target_star_header_index]) # We don't want this signal to interfere with out data
        #print(immediate_comparison_stars)
        
        if not ZTF_g_dataframe.empty:
            ax[column_index].plot((np.array(ZTF_g_dataframe["time"]) % period), (np.array(ZTF_g_dataframe[column_name]) / get_comparison_sums(ZTF_g_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_g_dataframe[column_name]) / get_comparison_sums(ZTF_g_dataframe, immediate_comparison_stars))), ".", color = "b", alpha = 0.3)
        if not ZTF_r_dataframe.empty:
            ax[column_index].plot((np.array(ZTF_r_dataframe["time"]) % period), (np.array(ZTF_r_dataframe[column_name]) / get_comparison_sums(ZTF_r_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_r_dataframe[column_name]) / get_comparison_sums(ZTF_r_dataframe, immediate_comparison_stars))), ".", color = "r", alpha = 0.3)
        if not ZTF_i_dataframe.empty:
            ax[column_index].plot((np.array(ZTF_i_dataframe["time"]) % period), (np.array(ZTF_i_dataframe[column_name]) / get_comparison_sums(ZTF_i_dataframe, immediate_comparison_stars)) / np.median((np.array(ZTF_i_dataframe[column_name]) / get_comparison_sums(ZTF_i_dataframe, immediate_comparison_stars))), ".", color = "brown", alpha = 0.3)
    
    column_index += 1
#'''


figure.text(0.5, 0, "Julian Days mod " + str(tic_ID) + " Period (OBJD)", ha = "center")
figure.text(0, 0.5, "Flux", va = "center", rotation = "vertical")
#figure.tight_layout()
plot.show()