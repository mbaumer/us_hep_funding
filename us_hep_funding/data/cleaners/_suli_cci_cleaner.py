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
