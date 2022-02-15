def plot_suli_state(statecode):

    fig = plt.figure()

    class LowerThreshold(ccrs.Mercator):
        @property
        def threshold(self):
            return 1

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
        facecolor = [0.9375, 0.9375, 0.859375]
        edgecolor = "black"

        if state.attributes["postal"] == statecode:
            ax.add_geometries(
                [state.geometry],
                ccrs.PlateCarree(),
                facecolor="Gold",
                edgecolor=edgecolor,
            )
        else:
            ax.add_geometries(
                [state.geometry],
                ccrs.PlateCarree(),
                facecolor=facecolor,
                edgecolor=edgecolor,
            )

    these_students = suli_students[suli_students["State"] == statecode]
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
            color="Blue",
            transform=ccrs.Geodetic(),
            alpha=alpha,
        )
    for index, college in college_counts.iterrows():
        student = (
            these_students[these_students["College"] == college["College"]]
            .reset_index()
            .loc[0]
        )
        popularity = 1.5 * college["Name"] + 5
        if index == 0:
            ax.plot(
                [],
                [],
                color="Blue",
                linestyle="None",
                label="Student Home Institutes",
                transform=ccrs.Geodetic(),
                markersize=10,
                marker=".",
                alpha=0.5,
            )
        ax.plot(
            student["Longitude"],
            student["Latitude"],
            color="Blue",
            transform=ccrs.Geodetic(),
            markersize=popularity,
            marker=".",
            alpha=0.5,
        )
    for i, lab in enumerate(these_students["Host Lab"].unique()):
        this_lab = natlabs[natlabs["Host Lab"] == lab]
        if i == 0:
            ax.plot(
                this_lab["Lab Longitude"],
                this_lab["Lab Latitude"],
                transform=ccrs.Geodetic(),
                marker="*",
                label="Host DOE National Labs",
                linestyle="None",
                markersize=10,
                color="Gold",
                markeredgewidth=1,
                markeredgecolor="Black",
            )
        else:
            ax.plot(
                this_lab["Lab Longitude"].values,
                this_lab["Lab Latitude"].values,
                transform=ccrs.Geodetic(),
                marker="*",
                markersize=10,
                color="Gold",
                markeredgewidth=1,
                markeredgecolor="Black",
            )

    ax.set_title(
        "Host National Laboratories for "
        + str(len(these_students))
        + " "
        + statecode
        + " SULI/CCI students (2014-2016)"
    )
    ax.legend()
    fig.savefig(
        "/Users/mbaumer/side_projects/us_hep_funding/docs/_img/" + statecode + ".png",
        format="png",
        bbox_inches="tight",
    )
    plt.close(fig)


def plot_suli_state_formal(statecode):
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

    these_students = suli_students[suli_students["State"] == statecode]
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
        this_lab = natlabs[natlabs["Host Lab"] == lab]
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
        "/Users/mbaumer/side_projects/us_hep_funding/docs/_img_formal/"
        + statecode
        + ".png",
        format="png",
        bbox_inches="tight",
        edgecolor="white",
        pad_inches=-0.1,
    )
