import os
import requests
import warnings

import numpy

from us_hep_funding.constants import RAW_DATA_PATH, SULI_STUDENT_URLS


class SuliStudentDataDownloader:
    def __init__(self):
        self.save_path = RAW_DATA_PATH / "unzipped"

    def run(self, fiscal_year: int):

        try:
            url = SULI_STUDENT_URLS[fiscal_year]
        except KeyError:
            print("Could not find key {0} in dict DOE_GRANTS_URLS".format(fiscal_year))
            return

        filename = url.split("/")[-1]
        if (self.save_path / filename).exists():
            return

        try:
            # suppress https warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                r = requests.get(url, allow_redirects=True, verify=False)
                r.raise_for_status()
        except:
            print("could not find", url)
            return

        zip_file_path = self.save_path / filename
        with (zip_file_path).open("wb+") as f:
            f.write(r.content)

        print("Data download for fiscal year {0} complete".format(fiscal_year))
