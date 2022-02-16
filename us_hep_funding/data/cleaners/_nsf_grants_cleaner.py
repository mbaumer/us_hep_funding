def clean_nsf_grant_data():
    print("Generating NSF Grant data...")

    contract_file_list = glob("../new_data/*049_Assistance*.csv")
    contract_df_list = []
    for contract_file in contract_file_list:
        df = pd.read_csv(contract_file)
        df["Year"] = contract_file.split("/")[-1][:4]
        contract_df_list.append(df)
    fulldata = pd.concat(contract_df_list, ignore_index=True)

    mps_grants = fulldata[
        fulldata["cfda_title"].map(str.strip).map(str.lower)
        == "mathematical and physical sciences"
    ]

    mps_grants = mps_grants[
        [
            "Year",
            "cfda_title",
            "federal_action_obligation",
            "recipient_state_code",
            "recipient_congressional_district",
            "recipient_name",
        ]
    ]

    mps_grants = mps_grants.rename(
        columns={
            "federal_action_obligation": "Amount ($)",
            "recipient_state_code": "State",
            "recipient_congressional_district": "District",
            "recipient_name": "Institution",
        }
    )

    mps_grants = mps_grants.dropna(subset=["District"])

    mps_grants["District"] = mps_grants["State"] + mps_grants["District"].map(int).map(
        str
    ).str.zfill(2)
    mps_grants.loc[mps_grants["District"] == "OR00", "State"] = "PR"
    mps_grants.loc[mps_grants["District"] == "OR00", "District"] = "PR00"

    mps_grants = mps_grants[mps_grants["Amount ($)"] > 0]
    mps_grants["Amount ($)"] = mps_grants["Amount ($)"].round(0)

    mps_insts = mps_grants["Institution"]
    mps_insts = mps_insts.str.replace("THE ", "")
    mps_insts = mps_insts.str.replace("REGENTS OF THE ", "")
    mps_insts = mps_insts.str.replace("PRESIDENT AND FELLOWS OF ", "")
    mps_insts = mps_insts.str.replace(" \(THE\)", "")
    mps_insts = mps_insts.str.replace("TRUSTEES OF ", "")
    mps_insts = mps_insts.str.replace(", THE$", "")
    mps_insts = mps_insts.str.replace(", INC$", "")
    mps_insts = mps_insts.str.replace(", INC.$", "")
    mps_insts = mps_insts.str.replace(" \(INC\)$", "")
    mps_insts = mps_insts.str.replace("FDN$", "Foundation")
    mps_insts = mps_insts.str.replace("ASTRON$", "Astronomy")
    mps_insts = mps_insts.str.replace(" \(THE\)$", "")
    mps_insts = mps_insts.str.replace(" INST ", " INSTITUTE ")
    mps_insts = mps_insts.str.replace("TECH$", "TECHNOLOGY")
    mps_insts = mps_insts.str.replace(",", "")
    mps_insts = mps_insts.str.replace(" INC$", "")
    mps_insts = mps_insts.str.replace("UNIV$", "UNIVERSITY")
    mps_insts = mps_insts.str.replace("MIT$", "MASSACHUSETTS INSTITUTE OF TECHNOLOGY")
    mps_insts = mps_insts.str.replace(" \(INC.\)$", "")
    mps_insts = mps_insts.str.replace("\d+$", "")
    mps_insts = mps_insts.str.replace("^U ", "UNIVERSITY ")
    mps_insts = mps_insts.str.replace(" CAL ", " CALIFORNIA ")
    mps_insts = mps_insts.str.replace("UNIVERSTIY", "UNIVERSITY")
    mps_insts = mps_insts.str.replace("UNIVER$", "UNIVERSITY")
    mps_insts = mps_insts.str.strip()
    mps_insts = mps_insts.str.title()
    mps_insts = mps_insts.str.replace("Csu", "CSU")
    mps_insts = mps_insts.str.replace("'S", "'s")
    mps_grants["Institution"] = mps_insts

    pd.to_pickle(mps_grants, "../new_data/cleaned/nsf_mps_grants.pkl")
