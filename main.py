import requests
import matplotlib.pyplot as plt
import json
import pandas as pd
import datetime as dt
from tkinter import *

START_YEAR = 1900
FINISH_YEAR = 2040

user_choice = None


def get_choice():
    global user_choice
    try:
        user_choice = int(entry.get())
    except ValueError:
        pass
    if user_choice == 1 or user_choice == 2:
        window.destroy()


# Make sure data does not attempt to extend beyond current year
now = dt.datetime.now()
if FINISH_YEAR >= now.year:
    FINISH_YEAR = now.year - 1

# Because sunspot data only goes to 1749, make sure data begins no earlier
if START_YEAR < 1749:
    START_YEAR = 1749

# Import solar cycle data from local file. If not available, import from SWPC and write to local file.
try:
    with open("solar_data_3.json") as file:
        sunspot_data = json.load(file)
except FileNotFoundError:
    sunspot_data = requests\
        .get("https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json").json()
    with open("solar_data_3.json", "w") as file:
        json.dump(sunspot_data, file)

# Import tornado data from local file. If not available, import from SPC and write to local file.
try:
    with open("tornado_data_3.csv") as file:
        tornado_table = pd.read_csv(file)
except FileNotFoundError:
    tornado_table = pd.read_csv("https://www.spc.noaa.gov/wcm/data/1950-2019_all_tornadoes.csv")
    tornado_table.to_csv("tornado_data_3.csv")

# Count number of tornadoes in each year and store in Pandas Series object
counts = tornado_table.value_counts("yr", ascending=True, sort=False)

# Create and fill dictionary of tornado counts
tornado_dict = {}
for (year, tornadoes) in counts.items():
    tornado_dict[str(year)] = tornadoes

# Create and fill dictionary of sunspot counts
sunspot_dict = {}
for year in range(START_YEAR, FINISH_YEAR + 1):
    sunspot_dict[str(year)] = 0
    for entry in sunspot_data:
        if str(year) in entry["time-tag"]:
            sunspot_dict[str(year)] += entry["ssn"]
    sunspot_dict[str(year)] = round(sunspot_dict[str(year)] / 12)

# Open window asking user whether they would like a line graph or scatter plot
window = Tk()
label = Label(text="Enter 1 for Tornado vs Sunspot scatter plot\nor 2 for Tornado and Sunspot vs Time line graph")
label.grid(column=0, row=0)
button = Button(text="Enter", command=get_choice)
button.grid(column=0, row=2)
entry = Entry()
entry.grid(column=0, row=1)
window.mainloop()

if user_choice == 1:
    plt.xlabel("Sunspot count")
    plt.ylabel("Tornado count")
    plt.title("Annual tornado count vs sunspot count")
    for (year, tors) in tornado_dict.items():
        try:
            x = sunspot_dict[str(year)]
            y = tors
            plt.scatter(x, y)
        except KeyError:
            pass
elif user_choice == 2:
    tornado_x = [int(year) for (year, tors) in tornado_dict.items()]
    sunspot_x = [int(year) for (year, sunspots) in sunspot_dict.items()]
    plt.plot(sunspot_x, sunspot_dict.values(), label="Sunspots")
    plt.plot(tornado_x, tornado_dict.values(), label="Tornadoes")
    x_axis_start = sunspot_x[0]
    x_axis_finish = sunspot_x[len(sunspot_x) - 1] + 1
    plt.xlim([x_axis_start, x_axis_finish])
    plt.xlabel("Year")
    plt.title("Annual tornado and sunspot count vs time")
    plt.legend()

# Show plot
plt.show()

# Print correlation coefficient to console
# print(np.corrcoef(annual_solar_averages[40:], tornado_counts[40:]))
