"""This will be the top-level API for producing updated
data tables."""
from datetime import datetime

from us_hep_funding.data.downloaders import (
    UsaSpendingDataDownloader,
    DoeDataDownloader,
    SuliStudentDataDownloader,
)
from us_hep_funding.data.cleaners import DoeContractDataCleaner, NsfGrantsCleaner

# # 2011 is as far as usaspending data goes back.
# # DOE grants go back to 2012.
YEARS_OF_INTEREST = range(2014, datetime.now().year + 1)

# usa_spending_downloader = UsaSpendingDataDownloader()
# doe_downloader = DoeDataDownloader()
suli_downloader = SuliStudentDataDownloader()

for fiscal_year in YEARS_OF_INTEREST:
    #     usa_spending_downloader.run(fiscal_year)
    #     doe_downloader.run(fiscal_year)
    suli_downloader.run(fiscal_year)

# doe_contract_cleaner = DoeContractDataCleaner()
# doe_contract_cleaner.run()

# nsf_grants_cleaner = NsfGrantsCleaner()
# nsf_grants_cleaner.run()
