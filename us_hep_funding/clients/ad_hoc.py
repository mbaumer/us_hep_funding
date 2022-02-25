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
