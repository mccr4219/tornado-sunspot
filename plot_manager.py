import matplotlib.pyplot as plt


class PlotManager:

    def show_plot(self, user_choice, tornado_dict, sunspot_dict):
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

