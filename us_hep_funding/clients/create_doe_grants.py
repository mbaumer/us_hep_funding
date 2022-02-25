import pandas as pd

from us_hep_funding.constants import CLEANED_DBS_PATH, RAW_DATA_PATH
from us_hep_funding.data.cleaners import DoeGrantsCleaner


def run():

    doe_grants2012 = DoeGrantsCleaner(
        RAW_DATA_PATH / "unzipped" / "DOE-SC_Grants_FY2012.xlsx",
        2012,
        sheet_name="DOE SC Awards FY 2012",
        amount_key="2012 Funding",
        program_office_key="SC Program",
        project_title_key="Project Title",
        pi_key="Principal Investigator(s)",
    ).run()

    doe_grants2013 = DoeGrantsCleaner(
        RAW_DATA_PATH / "unzipped" / "DOE-SC_Grants_FY2013.xlsx",
        2013,
        sheet_name="DOE SC Awards FY 2013",
        skiprows=1,
        district_key="Congressional District *",
        amount_key="FY 2013 Funding",
        program_office_key="SC Program",
        project_title_key="Project Title",
        pi_key="Principal Investigator(s)",
    ).run()

    doe_grants2014 = DoeGrantsCleaner(
        RAW_DATA_PATH / "unzipped" / "DOE-SC_Grants_FY2014.xlsx",
        2014,
        sheet_name="DOE SC Awards FY 2014",
        project_title_key="Project Title",
    ).run()

    doe_grants2015 = DoeGrantsCleaner(
        RAW_DATA_PATH / "unzipped" / "DOE-SC_Grants_FY2015.xlsx",
        2015,
        sheet_name="DOE SC Awards FY 2015",
        project_title_key="Project Title",
        state_key="State/Territory",
    ).run()

    doe_grants2016 = DoeGrantsCleaner(
        RAW_DATA_PATH / "unzipped" / "DOE-SC_Grants_FY2016.xlsx",
        2016,
        state_key="State/Territory",
    ).run()

    doe_grants2017 = DoeGrantsCleaner(
        RAW_DATA_PATH / "unzipped" / "DOE-SC_Grants_FY2017.xlsx",
        2017,
        pi_key="Principlal Investigator",
    ).run()

    doe_grants2018 = DoeGrantsCleaner(
        RAW_DATA_PATH / "unzipped" / "DOE-SC_Grants_FY2018.xlsx",
        2018,
        program_office_key="Program Office",
        pi_key="Principlal Investigator",
    ).run()

    doe_grants2019 = DoeGrantsCleaner(
        RAW_DATA_PATH / "unzipped" / "DOE-SC_Grants_FY2019.xlsx", 2019, pi_key="PI"
    ).run()

    doe_grants2020 = DoeGrantsCleaner(
        RAW_DATA_PATH / "unzipped" / "DOE-SC_Grants_FY2020.xlsx",
        2020,
        pi_key="PI",
    ).run()

    doe_grants2021 = DoeGrantsCleaner(
        RAW_DATA_PATH / "unzipped" / "SC-in-Your-State-FY-2021.xlsx", 2021, pi_key="PI"
    ).run()

    merged_df = pd.concat(
        [
            doe_grants2012,
            doe_grants2013,
            doe_grants2014,
            doe_grants2015,
            doe_grants2016,
            doe_grants2017,
            doe_grants2018,
            doe_grants2019,
            doe_grants2020,
            doe_grants2021,
        ]
    )

    merged_df.to_csv(CLEANED_DBS_PATH / "doe_grants.csv")


if __name__ == "__main__":
    run()
