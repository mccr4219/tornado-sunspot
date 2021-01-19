import requests
import pandas as pd
import json
import datetime as dt


class DataManager:

    def __init__(self):
        self.START_YEAR = 1940
        self.END_YEAR = 2040
        self.now = dt.datetime.now()

        # Make sure data does not attempt to extend beyond current year
        if self.END_YEAR >= self.now.year:
            self.END_YEAR = self.now.year - 1

        # Because sunspot data only goes to 1749, make sure data begins no earlier
        if self.START_YEAR < 1749:
            self.START_YEAR = 1749

        self.sunspot_data = {}
        self.sunspot_dict = {}
        self.tornado_table = {}
        self.tornado_counts = {}
        self.tornado_dict = {}

    # Import solar cycle data from local file. If not available, import from SWPC and write to local file.
    def import_solar_data(self):
        try:
            with open("solar_data.json") as file:
                self.sunspot_data = json.load(file)
        except FileNotFoundError:
            self.sunspot_data = requests \
                .get("https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json").json()
            with open("solar_data.json", "w") as file:
                json.dump(self.sunspot_data, file)

        # Fill dictionary of sunspot counts
        for year in range(self.START_YEAR, self.END_YEAR + 1):
            self.sunspot_dict[str(year)] = 0
            for entry in self.sunspot_data:
                if str(year) in entry["time-tag"]:
                    self.sunspot_dict[str(year)] += entry["ssn"]
            self.sunspot_dict[str(year)] = round(self.sunspot_dict[str(year)] / 12)
        return self.sunspot_dict

    def import_tornado_data(self):
        # Import tornado data from local file. If not available, import from SPC and write to local file.
        try:
            with open("tornado_data.csv") as file:
                self.tornado_table = pd.read_csv(file)
        except FileNotFoundError:
            self.tornado_table = pd.read_csv("https://www.spc.noaa.gov/wcm/data/1950-2019_all_tornadoes.csv")
            self.tornado_table.to_csv("tornado_data.csv")

        # Count number of tornadoes in each year and store in Pandas Series object
        self.tornado_counts = self.tornado_table.value_counts("yr", ascending=True, sort=False)

        # Create and fill dictionary of tornado counts
        for (year, tornadoes) in self.tornado_counts.items():
            self.tornado_dict[str(year)] = tornadoes
        return self.tornado_dict
