import os

import numpy


class DoeDataDownloader:
    def __init__(self):
        pass

    def run():
        pass


class UsaSpendingDownloader:
    def __init__():
        usaspending_base = (
            "https://www.usaspending.gov/download_center/award_data_archive"
        )
        save_path = "./raw_data/"
        datestr = "20220208"

    def run(fiscal_year: int):

        doe_contracts_url = (
            usaspending_base + str(FY) + "_089_Contracts_Full_" + datestr + ".zip"
        )
        doe_grants_url = (
            usaspending_base + str(FY) + "_089_Assistance_Full_" + datestr + ".zip"
        )
        nsf_grants_url = (
            usaspending_base + str(FY) + "_049_Assistance_Full_" + datestr + ".zip"
        )

        for url in [doe_contracts_url, doe_grants_url, nsf_grants_url]:

            filename = url.split("/")[-1]
            if os.path.exists(save_path + filename):
                continue

            try:
                r = requests.get(url, allow_redirects=True, verify=False)
                r.raise_for_status()
            except:
                print("could not find", url)
                continue

            open(save_path + filename, "wb+").write(r.content)
        print("Data download complete")


def unzip_all():
    for unzip_this in glob("../new_data/*.zip"):
        zipper = zipfile.ZipFile(unzip_this, "r")
        zipper.extractall(path="../new_data")
