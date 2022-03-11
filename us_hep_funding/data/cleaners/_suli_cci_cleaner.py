import camelot
import pandas as pd

_LAB_ABBRS_TO_NAMES = {
    "LBNL": "Lawrence Berkeley National Laboratory",
    "BNL": "Brookhaven National Laboratory",
    "ANL": "Argonne National Laboratory",
    "ORNL": "Oak Ridge National Laboratory",
    "NREL": "National Renewable Energy Laboratory",
    "PNNL": "Pacific Northwest National Laboratory",
    "LANL": "Los Alamos National Laboratory",
    "LLNL": "Lawrence Livermore National Laboratory",
    "AMES": "Ames National Laboratory",
    "INL": "Idaho National Laboratory",
    "PPPL": "Princeton Plasma Physics Laboratory",
    "SLAC": "SLAC National Accelerator Laboratory",
    "FNAL": "Fermi National Accelerator Laboratory",
    "TJNAF": "Thomas Jefferson National Accelerator Facility",
}

_NON_HEP_LABS = [
    "GA / DIII-D",
    "SNL NM",
    "SNL CA",
    "DOE Naval Reactors",
    "General Atomics / DIII-D",
    "Sandia National Laboratory",
]


class SuliStudentDataCleaner:
    def __init__(self, filepath, fiscal_year, column_remapper):
        self.fiscal_year = fiscal_year
        tables = camelot.read_pdf(filepath, flavor="stream", pages="all")
        for i, page in enumerate(tables):
            if i == 0:
                self.df = page.df
            else:
                self.df = pd.concat([self.df, page.df])
        print(self.df)
        self.df = self.df.rename(
            column_remapper,
            axis=1,
        )

    def _unify_formatting(self):
        if self.fiscal_year == 2020:
            # delete col headers that got merged together
            self.df = self.df[self.df["Term"] != "Term"]

            self.df["Name"] = self.df["First Name"] + " " + self.df["Last Name"]
            del self.df["First Name"], self.df["Last Name"]
            self.df["Host Lab"] = self.df["Host Lab"].map(_LAB_ABBRS_TO_NAMES)
        else:
            # delete col headers that got merged together
            self.df = self.df[self.df["Name"] != "SULI PARTICIPANT"]

            self.df["Term"] = self.df["Season"] + " " + self.df["Year"]
            del self.df["Season"], self.df["Year"]

            # delete trailing parenthetical lab name abbreviations
            self.df["Host Lab"] = self.df["Host Lab"].str.replace("\s\(\w*$", "")

    def run(self):

        self._unify_formatting()

        # delete rows with blanks which are fake table rows added by PDF reader
        self.df.replace("", float("NaN"), inplace=True)
        self.df.dropna(inplace=True)

        # drop students from obviously non-HEP labs
        self.df = self.df[~self.df["Host Lab"].isin(_NON_HEP_LABS)]

        self.df["Program"] = "SULI"

        self.df["Institution"] = self.df["Institution"].str.replace("\\xe2", "a")
        self.df["Name"] = self.df["Name"].str.replace("\\xe2", "a")
        self.df["Institution"] = self.df["Institution"].str.replace(
            "Stony Brook University", "State University of New York at Stony Brook"
        )
        print(self.df["Host Lab"].unique())
        return self.df
