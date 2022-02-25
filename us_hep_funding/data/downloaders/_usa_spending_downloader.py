"""Classes that download data from usaspending.gov"""

import pathlib
import warnings
import zipfile

import requests

from us_hep_funding.constants import (
    DOE_CONTRACTS_STR,
    NSF_GRANTS_STR,
    RAW_DATA_PATH,
    USASPENDING_BASEURL,
)


class UsaSpendingDataDownloader:
    """A downloader for getting data from usaspending.gov"""

    def __init__(self):
        self.base_url = USASPENDING_BASEURL
        self.save_path = RAW_DATA_PATH / "zips"
        self.unzip_path = RAW_DATA_PATH / "unzipped"

    def _run(self, fiscal_year: int, filestr: str):

        url = self.base_url + "FY" + str(fiscal_year) + filestr + ".zip"

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

        zipper = zipfile.ZipFile(zip_file_path, "r")
        zipper.extractall(path=str(self.unzip_path))

    def run(self, fiscal_year: int):

        self._run(fiscal_year, DOE_CONTRACTS_STR)
        self._run(fiscal_year, NSF_GRANTS_STR)

        print("Data download for fiscal year {0} complete".format(fiscal_year))
