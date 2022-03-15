import numpy as np
import matplotlib.pyplot as plt
import cartopy
import pandas as pd

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

from us_hep_funding.constants import CLEANED_DBS_PATH


class SuliStudentMapMaker:
    def __init__(self):
        geo_students = pd.read_csv(CLEANED_DBS_PATH / "suli_students_geocoded.csv")
        natlabs = pd.read_csv(CLEANED_DBS_PATH / "/national_labs_geocodio.csv")
        natlabs = natlabs[["Lab", "City", "Latitude", "Longitude"]].dropna()
        natlabs = natlabs.rename(
            columns={
                "Lab": "Host Lab",
                "City": "Lab City",
                "Latitude": "Lab Latitude",
                "Longitude": "Lab Longitude",
            }
        )

        self.natlabs = natlabs
        self.students = geo_students.merge(natlabs, on="Host Lab")

    def plot_suli_state_formal(self, statecode):
        class LowerThreshold(ccrs.Mercator):
            @property
            def threshold(self):
                return 1

        fig = plt.figure()

        if statecode == "HI":
            ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.LambertConformal())
            ax.set_extent([-165, -70, 20, 35], ccrs.Geodetic())
        elif statecode == "AK":
            ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.LambertConformal())
            ax.set_extent([-140, -66, 20, 77], ccrs.Geodetic())
        else:
            ax = fig.add_axes([0, 0, 1, 1], projection=LowerThreshold())
            ax.set_extent([-126, -66, 24.5, 46], ccrs.Geodetic())
        shapename = "admin_1_states_provinces_lakes_shp"
        states_shp = shpreader.natural_earth(
            resolution="110m", category="cultural", name=shapename
        )

        for state in shpreader.Reader(states_shp).records():
            # pick a default color for the land with a black outline,
            # this will change if the storm intersects with our track
            facecolor = "#C0C0C0"
            edgecolor = "white"

            if state.attributes["postal"] == statecode:
                ax.add_geometries(
                    [state.geometry],
                    ccrs.PlateCarree(),
                    facecolor="#A0A2A0",
                    edgecolor=edgecolor,
                    linewidth=0.5,
                )
            else:
                ax.add_geometries(
                    [state.geometry],
                    ccrs.PlateCarree(),
                    facecolor=facecolor,
                    edgecolor=edgecolor,
                    linewidth=0.5,
                )

        these_students = self.students[self.students["State"] == statecode]
        print(len(these_students))
        if len(these_students) < 20:
            alpha = 1
        elif len(these_students) < 80:
            alpha = 0.5
        else:
            alpha = 0.25

        unique_colleges = these_students["College"].unique()
        college_counts = these_students.groupby("College").count().reset_index()

        for idx in range(len(these_students)):
            student = these_students.iloc[idx]
            ax.plot(
                [student["Longitude"], student["Lab Longitude"]],
                [student["Latitude"], student["Lab Latitude"]],
                color="#D5422C",
                transform=ccrs.Geodetic(),
                alpha=alpha,
            )
        for i, lab in enumerate(these_students["Host Lab"].unique()):
            this_lab = self.natlabs[self.natlabs["Host Lab"] == lab]
            ax.plot(
                this_lab["Lab Longitude"].values,
                this_lab["Lab Latitude"].values,
                transform=ccrs.Geodetic(),
                marker="o",
                markersize=5,
                color="#D5422C",
                markeredgewidth=0,
                markeredgecolor="Black",
            )
        # plt.title('Host National Laboratories for '+str(len(these_students))+' '+statecode+' SULI/CCI students (2014-2016)')
        # plt.legend()
        fig.savefig(
            "/workspace/us_hep_funding" + statecode + ".png",
            format="png",
            bbox_inches="tight",
            edgecolor="white",
            pad_inches=-0.1,
        )


if __name__ == "__main__":
    mapper = SuliStudentMapMaker()
    mapper.plot_suli_state_formal("CA")
