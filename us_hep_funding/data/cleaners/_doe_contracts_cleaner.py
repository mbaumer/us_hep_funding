import pandas as pd

from us_hep_funding.constants import (
    CLEANED_DBS_PATH,
    RAW_DATA_PATH,
    SC_CONTRACTS_OFFICES,
)


class DoeContractDataCleaner:
    def __init__(self):
        self.contract_file_list = (RAW_DATA_PATH / "unzipped").glob(
            "*089_Contracts*.csv"
        )

    def _load_data(self):
        contract_df_list = []
        for contract_file in self.contract_file_list:
            df = pd.read_csv(contract_file)
            df["Year"] = contract_file.stem[2:6]
            df = df[
                (df["awarding_office_name"].isin(SC_CONTRACTS_OFFICES))
                | (df["funding_office_name"].isin(SC_CONTRACTS_OFFICES))
            ]
            contract_df_list.append(df)
        return pd.concat(contract_df_list, ignore_index=True)

    def _clean_data(self, sc_contracts: pd.DataFrame):

        sc_contracts = sc_contracts[
            [
                "award_id_piid",
                "federal_action_obligation",
                "recipient_name",
                "primary_place_of_performance_state_code",
                "primary_place_of_performance_congressional_district",
                "product_or_service_code_description",
                "Year",
            ]
        ]

        sc_contracts = sc_contracts.rename(
            columns={
                "federal_action_obligation": "Amount ($)",
                "award_id_piid": "award_id",
                "recipient_name": "Vendor",
                "primary_place_of_performance_state_code": "State",
                "primary_place_of_performance_congressional_district": "District",
                "product_or_service_code_description": "Item",
            }
        )

        sc_contracts = sc_contracts.dropna(subset=["District"])
        sc_contracts["District"] = sc_contracts["State"] + sc_contracts["District"].map(
            int
        ).map(str).str.zfill(2)
        sc_contracts = sc_contracts[sc_contracts["Amount ($)"] > 0]
        sc_contracts["Amount ($)"] = sc_contracts["Amount ($)"].round(0)

        vendors = sc_contracts["Vendor"]
        vendors = vendors.str.title()
        vendors = vendors.str.replace("'S", "'s")
        vendors = vendors.str.replace(" Limited Liability Company", ", LLC")
        vendors = vendors.str.replace("Llc", "LLC")
        vendors = vendors.str.replace("Incorporated", "Inc.")
        vendors = vendors.str.replace("It", "IT")
        vendors = vendors.str.replace("Pc", "PC")
        sc_contracts["Vendor"] = vendors

        items = sc_contracts["Item"]
        items = items.str.title()
        items = items.str.replace("Oper ", "Operation ")
        items = items.str.replace("Goco", "GOCO")
        items = items.str.replace("Gogo", "GOGO")
        items = items.str.replace("It", "IT")
        items = items.str.replace("Adpe", "ADPE")
        items = items.str.replace("Adp", "ADP")
        items = items.str.replace("Cpu", "CPU")
        sc_contracts["Item"] = items

        return sc_contracts

    def run(self):
        sc_contracts = self._load_data()
        cleaned_df = self._clean_data(sc_contracts)
        cleaned_df.to_csv(CLEANED_DBS_PATH / "test_contracts.csv", index=False)
