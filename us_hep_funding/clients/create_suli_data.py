import pandas as pd

from us_hep_funding.data.cleaners import SuliStudentDataCleaner


def run():

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

    merged = pd.concat([suli2019, suli2020])

    print(merged)


if __name__ == "__main__":
    run()
