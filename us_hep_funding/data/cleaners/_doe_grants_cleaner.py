import re

import numpy as np
import pandas as pd
from titlecase import titlecase


class DoeGrantsCleaner:
    def __init__(
        self,
        filepath,
        fiscal_year,
        sheet_name=0,
        skiprows=0,
        institution_key="Institution",
        district_key="Congressional District",
        amount_key="Awarded Amount",
        state_key="State",
        program_office_key="Organization",
        project_title_key="Title",
        award_number_key="Award Number",
        pi_key="Principal Investigator",
    ):

        self.data = pd.read_excel(filepath, sheet_name=sheet_name, skiprows=skiprows)

        # set weird column headings to uniform ones
        column_heading_remapper = {
            program_office_key: "SC Office",
            state_key: "State",
            district_key: "District",
            institution_key: "Institution",
            amount_key: "Amount ($)",
            project_title_key: "Project Title",
            pi_key: "Principal Investigator",
            award_number_key: "Award Number",
        }
        self.data.rename(columns=column_heading_remapper, inplace=True)

        # only keep relevant columns
        self.data = self.data[column_heading_remapper.values()]
        self.data["Year"] = fiscal_year * np.ones(len(self.data), dtype=int)
        print(fiscal_year)

    def run(self):
        hepdata = self._get_hep_grants()
        return self._clean_data(hepdata)

    def _get_hep_grants(self):

        agencies = self.data["SC Office"].values
        abbrev_agencies = []
        for entry in list(agencies):
            test = re.split(r"\(|\)", str(entry))
            if len(test) > 1:
                abbrev_agencies.append(test[1])
            else:
                abbrev_agencies.append(entry)
        self.data["SC Office"] = abbrev_agencies

        return self.data[
            (self.data["SC Office"] == "HEP")
            | (self.data["SC Office"] == "High Energy Physics")
        ]

    @staticmethod
    def _clean_data(hepdata):

        # strip out whitespace
        hepdata["State"] = hepdata["State"].map(str).map(str.strip)

        hepdata = hepdata.dropna(subset=["Amount ($)"])
        hepdata["Project Title"].replace("&#8208;", "-", inplace=True)
        # unicode problems in the raw data
        hepdata["Project Title"].loc[
            1675
        ] = "High Energy Physics - Energy, Intensity, Theoretical Frontier"
        hepdata["Project Title"].loc[
            4357
        ] = "High Energy Physics - Energy, Intensity, Theoretical Frontier"

        # clean up institute names
        insts = hepdata["Institution"]
        insts = insts.str.encode("ascii").map(str)
        insts = insts.str.strip()

        insts = insts.map(titlecase)

        insts = insts.str.replace(" At ", " - ")
        insts = insts.str.replace(", ", " - ")
        insts = insts.str.replace("U. ", "University ")
        insts = insts.str.replace("Inst. ", "Institute ")
        insts = insts.str.replace("Cuny", "CUNY")
        insts = insts.str.replace("Suny", "SUNY")
        insts = insts.str.replace(
            "University Of Illinois - Urbana-Champain",
            "University Of Illinois - Urbana-Champaign",
        )
        insts = insts.str.replace("Llc", "LLC")
        insts = insts.str.replace("Ieee", "IEEE")
        insts = insts.str.replace("Mit", "MIT")
        insts = insts.str.replace(
            "City College Of New York \(CUNY\) - Queens College",
            "CUNY - Queens College",
        )
        insts = insts.str.replace(
            "State University Of New York \(SUNY\) - Albany", "SUNY - Albany"
        )
        insts = insts.str.replace(
            "Virginia Polytechnic Institute And State University \(Virginia Tech\)",
            "Virginia Tech University",
        )
        insts = insts.str.replace(
            "Virginia Polytechnic Institute And State University",
            "Virginia Tech University",
        )
        insts = insts.str.replace(
            "Virginia Tech \(Virginia Tech\)", "Virginia Tech University"
        )

        insts = insts.str.replace("Univ\.", "University")
        insts = insts.str.replace(
            "State University Of New York - Stony Brook", "SUNY - Stony Brook"
        )
        insts = insts.str.replace(
            "City University Of New York - York College", "CUNY - York College"
        )
        insts = insts.str.replace(
            "State University Of New York - Albany", "SUNY - Albany"
        )
        insts = insts.str.replace("Virginia - University Of", "University of Virginia")
        insts = insts.str.replace(
            "College Ofwilliam And Mary", "College Of William And Mary"
        )

        insts = insts.str.replace(
            "California Institute Of Technology \(Caltech\)",
            "California Institute Of Technology",
        )
        insts = insts.str.replace("Harvard College", "Harvard University")
        insts = insts.str.replace(
            "Louisiana State University And A&M College", "Louisiana State University"
        )
        insts = insts.str.replace(
            "Iowa State University Of Science And Technology", "Iowa State University"
        )
        insts = insts.str.replace(
            "Massachusetts Institute Of Technology \(MIT\)",
            "Massachusetts Institute Of Technology",
        )
        insts = insts.str.replace(
            "Old Dominion University Research Foundation", "Old Dominion University"
        )
        insts = insts.str.replace(
            "President And Fellows Of Harvard College", "Harvard University"
        )
        insts = insts.str.replace("SUNY - Stony Brook University", "SUNY - Stony Brook")
        insts = insts.str.replace(
            "Research Foundation Of The City University Of New York \(CUNY\)",
            "CUNY Research Foundation",
        )
        insts = insts.str.replace(
            "Rutgers University - New Brunswick", "Rutgers University"
        )
        insts = insts.str.replace(
            "Rutgers University, New Brunswick", "Rutgers University"
        )
        insts = insts.str.replace(
            "Rutgers - State University Of New Jersey - New Brunswick",
            "Rutgers University",
        )
        insts = insts.str.replace(
            "Rutgers - The State University Of New Jersey", "Rutgers University"
        )
        insts = insts.str.replace(
            "Rutgers - The State University Of New Jersey - New Brunswick",
            "Rutgers University",
        )

        # honestly i have no idea why this needs to happen twice!
        insts = insts.str.replace(
            "Rutgers University - New Brunswick", "Rutgers University"
        )
        insts = insts.str.replace(
            "Rutgers University, New Brunswick", "Rutgers University"
        )
        insts = insts.str.replace(
            "Rutgers - State University Of New Jersey - New Brunswick",
            "Rutgers University",
        )
        insts = insts.str.replace(
            "Rutgers - The State University Of New Jersey", "Rutgers University"
        )
        insts = insts.str.replace(
            "Rutgers - The State University Of New Jersey - New Brunswick",
            "Rutgers University",
        )
        #

        insts = insts.str.replace(
            "Smithsonian Institute - Smithsonian Astrophysical Observatory",
            "Smithsonian Astrophysical Observatory",
        )
        insts = insts.str.replace(
            "Smithsonian Institute /Smithsonian Astrophysical Observatory",
            "Smithsonian Astrophysical Observatory",
        )
        insts = insts.str.replace(
            "Texas A&M Research Foundation", "Texas A&M University"
        )
        insts = insts.str.replace(
            "Texas A&M University - College Station", "Texas A&M University"
        )
        insts = insts.str.replace(
            "Texas A&M University, College Station", "Texas A&M University"
        )
        insts = insts.str.replace("University - Albany \(SUNY\)", "SUNY - Albany")
        insts = insts.str.replace("SUNY - University - Albany", "SUNY - Albany")
        insts = insts.str.replace("SUNY - University Of Albany", "SUNY - Albany")
        insts = insts.str.replace("Brandies University", "Brandeis University")
        insts = insts.str.replace(
            "University Of Notre Dame Du Lac", "University Of Notre Dame"
        )
        insts = insts.str.replace(
            "University Of Washington - Seattle", "University Of Washington"
        )
        insts = insts.str.replace(
            "Stony Brook University \(SUNY\)", "SUNY - Stony Brook"
        )
        insts = insts.str.replace(
            "State University Of New York \(SUNY\) - Albany", "SUNY - Albany"
        )
        insts = insts.str.replace("York College \(CUNY\)", "CUNY - York College")
        insts = insts.str.replace("William Marsh Rice University", "Rice University")
        insts = insts.str.replace(
            "Michigan Technological University", "Michigan Tech. University"
        )
        insts = insts.str.replace(
            "President And Fellows Of Harvard University", "Harvard University"
        )
        insts = insts.str.replace(
            "University Of Tennessee - Knoxville", "University Of Tennessee"
        )
        insts = insts.str.replace(
            "Indiana University - Bloomington", "Indiana University"
        )
        insts = insts.str.replace(
            "University Of Alabama - Tuscaloosa", "University Of Alabama"
        )
        insts = insts.str.replace(
            "State University Of New York \(SUNY\) - Stony Brook", "SUNY - Stony Brook"
        )
        insts = insts.str.replace(
            "Rensselaer Polytechnic Institute", "Rensselaer Polytechnic Inst."
        )
        insts = insts.str.replace(
            "University Of  Texas - Arlington", "University Of Texas - Arlington"
        )
        insts = insts.str.replace(
            "Virginia Polytechnic Institute", "Virginia Tech University"
        )
        insts = insts.str.replace(" Of ", " of ")
        insts = insts.str.replace(" In ", " in ")

        hepdata["Institution"] = insts

        return hepdata
