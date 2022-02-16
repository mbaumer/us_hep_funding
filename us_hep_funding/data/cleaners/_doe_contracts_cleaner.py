def clean_doe_contract_data():
    print("Generating DOE Contract data...")

    contract_file_list = glob("../new_data/*089_Contracts*.csv")
    contract_df_list = []
    for contract_file in contract_file_list:
        df = pd.read_csv(contract_file)
        df["Year"] = contract_file.split("/")[-1][:4]
        contract_df_list.append(df)
    fulldata = pd.concat(contract_df_list, ignore_index=True)

    sc_awarding_offices = [
        "CHICAGO SERVICE CENTER (OFFICE OF SCIENCE)",
        "OAK RIDGE OFFICE (OFFICE OF SCIENCE)",
        "SC CHICAGO SERVICE CENTER",
        "SC OAK RIDGE OFFICE",
    ]

    sc_funding_offices = [
        "CHICAGO SERVICE CENTER (OFFICE OF SCIENCE)",
        "OAK RIDGE OFFICE (OFFICE OF SCIENCE)",
        "SCIENCE",
        "SC OAK RIDGE OFFICE",
        "SC CHICAGO SERVICE CENTER",
    ]

    sc_contracts = fulldata[
        (fulldata["awarding_office_name"].isin(sc_awarding_offices))
        | (fulldata["funding_office_name"].isin(sc_funding_offices))
    ]

    # Clean data

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

    sc_contracts.to_pickle("../new_data/cleaned/sc_contracts.pkl")
