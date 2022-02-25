"""Constants for configuring us_hep_funding"""
import pathlib

RAW_DATA_PATH = pathlib.Path("/workspaces/us_hep_funding/raw_data/")
CLEANED_DBS_PATH = pathlib.Path("/workspaces/us_hep_funding/cleaned_data/")

USASPENDING_BASEURL = "https://files.usaspending.gov/award_data_archive/"
DOE_CONTRACTS_STR = "_089_Contracts_Full_20220208"
NSF_GRANTS_STR = "_049_Assistance_Full_20220208"

# have to be explicit about these since DOE changes the file names in some years.
DOE_GRANTS_URLS = {
    2012: "https://science.osti.gov/-/media/_/excel/universities/DOE-SC_Grants_FY2012.xlsx",
    2013: "https://science.osti.gov/-/media/_/excel/universities/DOE-SC_Grants_FY2013.xlsx",
    2014: "https://science.osti.gov/-/media/_/excel/universities/DOE-SC_Grants_FY2014.xlsx",
    2015: "https://science.osti.gov/-/media/_/excel/universities/DOE-SC_Grants_FY2015.xlsx",
    2016: "https://science.osti.gov/-/media/_/excel/universities/DOE-SC_grants_FY2016.xlsx",
    2017: "https://science.osti.gov/-/media/_/excel/universities/DOE-SC_grants_FY2017.xlsx",
    2018: "https://science.osti.gov/-/media/_/excel/universities/DOE-SC_Grants_FY2018.xlsx",
    2019: "https://science.osti.gov/-/media/_/excel/universities/DOE-SC_Grants_FY2019.xlsx",
    2020: "https://science.osti.gov/-/media/_/excel/universities/DOE-SC_Grants_FY2020.xlsx",
    2021: "https://science.osti.gov/-/media/_/excel/universities/SC-in-Your-State-FY-2021.xlsx",
}

SC_CONTRACTS_OFFICES = [
    "CHICAGO SERVICE CENTER (OFFICE OF SCIENCE)",
    "OAK RIDGE OFFICE (OFFICE OF SCIENCE)",
    "SCIENCE",
    "SC OAK RIDGE OFFICE",
    "SC CHICAGO SERVICE CENTER",
]
