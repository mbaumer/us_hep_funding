import pandas as pd

from us_hep_funding.constants import CLEANED_DBS_PATH
from us_hep_funding.data.cleaners import SuliStudentDataCleaner


def run():

    suli2014 = SuliStudentDataCleaner(
        "/workspaces/us_hep_funding/raw_data/unzipped/2014-SULI-Terms_Participant-Report.pdf",
        2014,
        {
            0: "Name",
            1: "Institution",
            2: "Host Lab",
            3: "Term",
        },
    ).run()

    suli2015 = SuliStudentDataCleaner(
        "/workspaces/us_hep_funding/raw_data/unzipped/2015-SULI-Terms_Participant-Report.pdf",
        2015,
        {0: "Name", 1: "Institution", 2: "Host Lab", 3: "Term"},
    ).run()

    suli2016 = SuliStudentDataCleaner(
        "/workspaces/us_hep_funding/raw_data/unzipped/2016-SULI-Terms_Participant-Report.pdf",
        2016,
        {
            0: "Name",
            1: "Institution",
            2: "Host Lab",
            3: "Term",
        },
    ).run()

    suli2017 = SuliStudentDataCleaner(
        "/workspaces/us_hep_funding/raw_data/unzipped/SULI-participants-2017.pdf",
        2017,
        {
            0: "Name",
            1: "Institution",
            2: "Host Lab",
            3: "Season",
            4: "Year",
        },
    ).run()

    suli2018 = SuliStudentDataCleaner(
        "/workspaces/us_hep_funding/raw_data/unzipped/SULI-participants-2018_a.pdf",
        2018,
        {
            0: "Name",
            1: "Institution",
            2: "Host Lab",
            3: "Season",
            4: "Year",
        },
    ).run()

    suli2019 = SuliStudentDataCleaner(
        "/workspaces/us_hep_funding/raw_data/unzipped/SULI-participants-2019.pdf",
        2019,
        {
            0: "Name",
            1: "Institution",
            2: "Host Lab",
            3: "Season",
            4: "Year",
        },
    ).run()

    suli2020 = SuliStudentDataCleaner(
        "/workspaces/us_hep_funding/raw_data/unzipped/2020-SULI-participants.pdf",
        2020,
        {
            0: "Term",
            1: "First Name",
            2: "Last Name",
            3: "Institution",
            4: "Host Lab",
        },
    ).run()

    merged = pd.concat(
        [suli2014, suli2015, suli2016, suli2017, suli2018, suli2019, suli2020],
        ignore_index=True,
    )

    merged.to_csv(CLEANED_DBS_PATH / "suli_students.csv")


def geocode():
    df = pd.read_csv(CLEANED_DBS_PATH / "suli_students.csv")
    geocodes = pd.read_csv(CLEANED_DBS_PATH / "geocodes.csv")

    merged = df.merge(geocodes, left_on="Institution", right_on="College", how="inner")

    natlabs = pd.read_csv(CLEANED_DBS_PATH / "national_labs_geocodio.csv")
    natlabs = natlabs[["Lab", "City", "Latitude", "Longitude"]].dropna()
    natlabs = natlabs.rename(
        columns={
            "Lab": "Host Lab",
            "City": "Lab City",
            "Latitude": "Lab Latitude",
            "Longitude": "Lab Longitude",
        }
    )
    geo_students = merged.merge(natlabs, on="Host Lab")

    print(len(merged), len(geo_students))

    geo_students.to_csv(CLEANED_DBS_PATH / "suli_students_geocoded.csv")


if __name__ == "__main__":
    geocode()
