from window_manager import WindowManager
from plot_manager import PlotManager
from data_manager import DataManager
import numpy as np

# Open window asking user whether they would like a line graph or scatter plot
window_manager = WindowManager()
user_choice = window_manager.user_choice
plot_manager = PlotManager()
data_manager = DataManager()
tornado_dict = data_manager.import_tornado_data()
sunspot_dict = data_manager.import_solar_data()

plot_manager.show_plot(user_choice=user_choice, tornado_dict=tornado_dict, sunspot_dict=sunspot_dict)

# NOT CURRENTLY WORKING - Print correlation coefficient to console
# print(np.corrcoef(annual_solar_averages[40:], tornado_counts[40:]))
