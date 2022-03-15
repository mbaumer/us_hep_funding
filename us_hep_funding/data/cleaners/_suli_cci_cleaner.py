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
        self.df = self.df.rename(
            column_remapper,
            axis=1,
        )

    def _unify_formatting(self):

        if "First Name" in self.df.columns:
            self.df["Name"] = self.df["First Name"] + " " + self.df["Last Name"]
            del self.df["First Name"], self.df["Last Name"]

        if "Season" in self.df.columns:
            self.df["Term"] = self.df["Season"] + " " + self.df["Year"]
            del self.df["Season"], self.df["Year"]

    def run(self):

        # delete rows with blanks which are fake table rows added by PDF reader
        self.df.replace("", float("NaN"), inplace=True)
        self.df.dropna(inplace=True)

        self.df.drop_duplicates(inplace=True, keep=False)

        self._unify_formatting()

        self.df["Institution"] = self.df["Institution"].str.normalize("NFKD")
        self.df["Host Lab"] = self.df["Host Lab"].str.normalize("NFKD")

        # delete trailing parenthetical lab name abbreviations
        self.df["Host Lab"] = (
            self.df["Host Lab"].str.replace("\(\w*\)$", "").str.rstrip()
        )

        # drop students from obviously non-HEP labs
        self.df = self.df[~self.df["Host Lab"].isin(_NON_HEP_LABS)]

        # some years list only lab abbreviations rather than names
        if self.df["Host Lab"].isin(_LAB_ABBRS_TO_NAMES.keys()).all():
            self.df["Host Lab"] = self.df["Host Lab"].map(_LAB_ABBRS_TO_NAMES)

        self.df["Program"] = "SULI"

        self.df["Institution"] = self.df["Institution"].str.replace(
            "Stony Brook University", "State University of New York at Stony Brook"
        )
        return self.df
