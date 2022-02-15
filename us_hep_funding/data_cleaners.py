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


def clean_doe_grant_data():
    print("Generating DOE Grant data...")
    dataB = pd.read_excel("../new_data/DOE-SC_Grants_FY2019.xlsx")
    dataB[dataB["Awarded Amount"] == "Other Mod"] = 0
    dataA = pd.read_excel("../new_data/DOE-SC_Grants_FY2018.xlsx")
    data0 = pd.read_excel("../new_data/DOE-SC_Grants_FY2017.xlsx")
    data = pd.read_excel("../new_data/DOE-SC_Grants_FY2016.xlsx")
    data2 = pd.read_excel(
        "../new_data/DOE-SC_Grants_FY2015.xlsx", sheet_name="DOE SC Awards FY 2015"
    )
    data3 = pd.read_excel(
        "../new_data/DOE-SC_Grants_FY2014.xlsx", sheet_name="DOE SC Awards FY 2014"
    )
    data4 = pd.read_excel(
        "../new_data/DOE-SC_Grants_FY2013.xlsx",
        sheet_name="DOE SC Awards FY 2013",
        skiprows=1,
    )
    data5 = pd.read_excel(
        "../new_data/DOE-SC_Grants_FY2012.xlsx", sheet_name="DOE SC Awards FY 2012"
    )

    ### FIXES TO RAW DATA
    data2.loc[
        data2["Institution"] == "University of Minnesota", "Congressional District"
    ] = "MN-05"
    data4.loc[
        data4["Institution"] == "CALIFORNIA INST. OF TECHNOLOGY",
        "Congressional District *",
    ] = "CA-27"
    data3.loc[
        data3["Institution"] == "California Institute of Technology (CalTech)",
        "Congressional District",
    ] = "CA-27"
    data2.loc[
        data2["Institution"] == "California Institute of Technology",
        "Congressional District",
    ] = "CA-27"
    data.loc[
        data["Institution"] == "California Institute of Technology",
        "Congressional District",
    ] = "CA-27"
    data0.loc[
        data0["Institution"] == "California Institute of Technology",
        "Congressional District",
    ] = "CA-27"
    dataA.loc[
        dataA["Institution"] == "California Institute of Technology",
        "Congressional District",
    ] = "CA-27"
    # this bug was fixed in FY2019 data
    ### END FIXES

    institutions = pd.concat(
        [
            dataB["Institution"],
            dataA["Institution"],
            data0["Institution"],
            data["Institution"],
            data2["Institution"],
            data3["Institution"],
            data4["Institution"],
            data5["Institution"],
        ],
        ignore_index=True,
        axis=0,
    )
    districts = pd.concat(
        [
            dataB["Congressional District"],
            dataA["Congressional District"],
            data0["Congressional District"],
            data["Congressional District"],
            data2["Congressional District"],
            data3["Congressional District"],
            data4["Congressional District *"],
            data5["Congressional District"],
        ],
        ignore_index=True,
        axis=0,
    )
    amounts = pd.concat(
        [
            dataB["Awarded Amount"],
            dataA["Awarded Amount"],
            data0["Awarded Amount"],
            data["Awarded Amount"],
            data2["Awarded Amount"],
            data3["Awarded Amount"],
            data4["FY 2013 Funding"],
            data5["2012 Funding"],
        ],
        ignore_index=True,
        axis=0,
    )
    years = pd.Series(
        np.concatenate(
            [
                2019 * np.ones(len(dataB), dtype=int),
                2018 * np.ones(len(dataA), dtype=int),
                2017 * np.ones(len(data0), dtype=int),
                2016 * np.ones(len(data), dtype=int),
                2015 * np.ones(len(data2), dtype=int),
                2014 * np.ones(len(data3), dtype=int),
                2013 * np.ones(len(data4), dtype=int),
                2012 * np.ones(len(data5), dtype=int),
            ]
        )
    )
    states = pd.concat(
        [
            dataB["State"],
            dataA["State"],
            data0["State"],
            data["State/Territory"],
            data2["State/Territory"],
            data3["State"],
            data4["State"],
            data5["State"],
        ],
        ignore_index=True,
        axis=0,
    )
    programs = pd.concat(
        [
            dataB["Organization"],
            dataA["Program Office"],
            data0["Organization"],
            data["Organization"],
            data2["Organization"],
            data3["Organization"],
            data4["SC Program"],
            data5["SC Program"],
        ],
        ignore_index=True,
        axis=0,
    )
    titles = pd.concat(
        [
            dataB["Title"],
            dataA["Title"],
            data0["Title"],
            data["Title"],
            data2["Project Title"],
            data3["Project Title"],
            data4["Project Title"],
            data5["Project Title"],
        ],
        ignore_index=True,
        axis=0,
    )
    award_nums = pd.concat(
        [
            dataB["Award Number"],
            dataA["Award Number"],
            data0["Award Number"],
            data["Award Number"],
            data2["Award Number"],
            data3["Award Number"],
            data4["Award Number"],
            data5["Award Number"],
        ],
        ignore_index=True,
        axis=0,
    )

    pis = pd.concat(
        [
            dataB["PI"],
            dataA["Principlal Investigator"],
            data0["Principlal Investigator"],
            data["Principal Investigator"],
            data2["Principal Investigator"],
            data3["Principal Investigator"],
            data4["Principal Investigator(s)"],
            data5["Principal Investigator(s)"],
        ],
        ignore_index=True,
        axis=0,
    )

    fulldata = pd.concat(
        [
            programs,
            years,
            states,
            districts,
            institutions,
            amounts,
            titles,
            pis,
            award_nums,
        ],
        axis=1,
        keys=[
            "SC Office",
            "Year",
            "State",
            "District",
            "Institution",
            "Amount ($)",
            "Project Title",
            "Principal Investigator",
            "Award Number",
        ],
    )

    fulldata["State"] = fulldata["State"].map(str).map(str.strip)

    agencies = fulldata["SC Office"].values
    abbrev_agencies = []
    for entry in list(agencies):
        test = re.split(r"\(|\)", str(entry))
        if len(test) > 1:
            abbrev_agencies.append(test[1])
        else:
            abbrev_agencies.append(entry)
    fulldata["SC Office"] = abbrev_agencies

    hepdata = fulldata[
        (fulldata["SC Office"] == "HEP")
        | (fulldata["SC Office"] == "High Energy Physics")
    ]
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
    insts = insts.str.encode("ascii")
    insts = insts.str.strip()

    assert insts.str.contains("'").sum() == 0  # safe to use.title()

    insts = insts.str.title()
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
        "City College Of New York \(CUNY\) - Queens College", "CUNY - Queens College"
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
    insts = insts.str.replace("State University Of New York - Albany", "SUNY - Albany")
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
    insts = insts.str.replace("Rutgers University, New Brunswick", "Rutgers University")
    insts = insts.str.replace(
        "Rutgers - State University Of New Jersey - New Brunswick", "Rutgers University"
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
    insts = insts.str.replace("Rutgers University, New Brunswick", "Rutgers University")
    insts = insts.str.replace(
        "Rutgers - State University Of New Jersey - New Brunswick", "Rutgers University"
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
    insts = insts.str.replace("Texas A&M Research Foundation", "Texas A&M University")
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
    insts = insts.str.replace("Stony Brook University \(SUNY\)", "SUNY - Stony Brook")
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
    insts = insts.str.replace("Indiana University - Bloomington", "Indiana University")
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

    hepdata.to_pickle("../new_data/cleaned/hep_grants.pkl")


def clean_suli_student_data():
    geocoded_insts = pd.read_csv(
        "/Users/mbaumer/side_projects/us_hep_funding/newdata2020/college_addresses_geocodio_2020.csv"
    )

    data = pd.read_csv(
        "/Users/mbaumer/Documents/HEP Advocacy/suli_student_data.csv",
        names=["Name", "College", "Host Lab", "Term", "A", "B"],
        skiprows=1,
    )
    data = data[["Name", "College", "Host Lab", "Term"]]

    data["Program"] = "SULI"
    data = data.dropna()
    data = data.replace("\\n", "", regex=True)

    data = data.append(
        pd.DataFrame(
            np.array(
                [
                    ["Reed Bowles"],
                    ["Wichita State University"],
                    ["Fermi National Accelerator Laboratory"],
                    ["Summer 2017"],
                ]
            ).T,
            columns=["Name", "College", "Host Lab", "Term"],
        ),
        ignore_index=True,
    )

    data2 = pd.read_csv(
        "/Users/mbaumer/side_projects/us_hep_funding/newdata2020/cci_student_info.csv",
        names=["Name", "College", "Host Lab", "Term", "A", "B"],
        skiprows=1,
    )
    data2 = data2[["Name", "College", "Host Lab", "Term"]]
    data2["Program"] = "CCI"
    data2 = data2.dropna()
    data2 = data2.replace("\\n", "", regex=True)

    data = pd.concat([data, data2], ignore_index=True)

    print(len(data))

    data["College"] = data["College"].str.replace("\\xe2", "a")
    data["Name"] = data["Name"].str.replace("\\xe2", "a")
    data["College"] = data["College"].str.replace(
        "Stony Brook University", "State University of New York at Stony Brook"
    )

    geo_students = data.merge(geocoded_insts)

    geo_students["Name"].loc[452] = "Angelica Tirado"
    geo_students["Name"].loc[455] = "Keishla Marie Sanchez Ortiz"
    geo_students["Name"].loc[473] = "Nneka Estee Joyette-Daniel"
    geo_students["Name"].loc[2686] = "Amanda Sofia Caballero"
    geo_students["Name"].loc[3060] = "Nataniel Medina Berrios"
    geo_students["Name"].loc[3417] = "Rubi Pena"

    print("total suli", len(geo_students))

    pd.to_pickle(
        geo_students,
        "/Users/mbaumer/side_projects/us_hep_funding/new_data/cleaned/suli_students.pkl",
    )


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


def clean_fnal_procurements():
    # for i in range(4,54):
    #     if i == 4:
    #         fnal = pd.read_excel('/Users/mbaumer/Downloads/FY\'18 Purchases by Supplier_State_All_states.xlsm',sheet_name=i)
    #     else:
    #         fnal = fnal.append(pd.read_excel('/Users/mbaumer/Downloads/FY\'18 Purchases by Supplier_State_All_states.xlsm',sheet_name=i))
    # fnal = fnal.dropna()
    # fnal_geo = pd.read_csv('../data/fnal_vendors_final_geocodio.csv')
    # fnal_geo = fnal_geo[['ZIP','Congressional District']]
    # fnal_geo = fnal_geo.dropna()
    # labeled = fnal.merge(fnal_geo)
    print("cleaning FNAL procurements")

    labeled = pd.read_csv("~/Downloads/fnal_19_geocodio_done.csv")
    labeled = labeled[-labeled["POTotal"].str.contains("\$")]

    labeled["Congressional District"] = labeled["Congressional District"].str.replace(
        "[A-Z][A-Z]", ""
    )
    labeled = labeled[
        ["VENDOR_NAME", "STATE", "ZIP", "Congressional District", "POTotal"]
    ]
    labeled = labeled.dropna()
    labeled["ZIP"] = labeled["ZIP"].str.replace("-\d+$", "")
    labeled = labeled.rename(
        columns={
            "VENDOR_NAME": "Vendor",
            "STATE": "State",
            "Congressional District": "District",
            "POTotal": "Amount ($)",
            "ZIP": "ZIP Code",
        }
    )
    labeled["Vendor"] = labeled["Vendor"].str.title()
    labeled["Vendor"] = labeled["Vendor"].str.replace("Llc", "LLC")
    labeled["Vendor"] = labeled["Vendor"].str.replace("'S", "'s")
    labeled["Vendor"] = labeled["Vendor"].str.replace(" Of ", " of ")
    labeled["Vendor"] = labeled["Vendor"].str.replace(" In ", " in ")
    labeled["int_amount"] = labeled["Amount ($)"].astype(float)
    labeled["Amount ($)"] = labeled["Amount ($)"].astype(float).map("${:,.0f}".format)
    labeled["ZIP Code"] = labeled["ZIP Code"].astype(int).astype(str)
    pd.to_pickle(labeled, "../new_data/cleaned/fnal_procurements.pkl")
