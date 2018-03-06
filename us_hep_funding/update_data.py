import re
import numpy as np
import pandas as pd
import yaml


def clean_doe_contract_data():
    print 'Generating DOE Contract data...'
    data1 = pd.read_csv(
        '../data/doe_contracts/2018_DOE_Contracts_Full_20180115.csv')
    data2 = pd.read_csv(
        '../data/doe_contracts/2017_DOE_Contracts_Full_20180115.csv')
    data3 = pd.read_csv(
        '../data/doe_contracts/2016_DOE_Contracts_Full_20180115.csv')
    data4 = pd.read_csv(
        '../data/doe_contracts/2015_DOE_Contracts_Full_20180115.csv')
    data5 = pd.read_csv(
        '../data/doe_contracts/2014_DOE_Contracts_Full_20180115.csv')
    data6 = pd.read_csv(
        '../data/doe_contracts/2013_DOE_Contracts_Full_20180115.csv')
    data7 = pd.read_csv(
        '../data/doe_contracts/2012_DOE_Contracts_Full_20180115.csv')

    fulldata = pd.concat([data1, data2, data3, data4, data5, data6, data7])

    sc_offices = ['00002: CHICAGO SERVICE CENTER (OFFICE OF SCIENCE)',
                  '00005: OAK RIDGE OFFICE (OFFICE OF SCIENCE)', '892431: SC OAK RIDGE OFFICE', '892401: SCIENCE',
                  '892430: SC CHICAGO SERVICE CENTER', '892430: SE-SC CHICAGO SERVICE CENTER', '892401: SE-SCIENCE FUNDS']
    sc_contracts = fulldata[(fulldata['fundingrequestingofficeid'].isin(
        sc_offices)) | (fulldata['contractingofficeid'].isin(sc_offices))]

    sc_contracts.to_pickle('../cleaned_data/sc_contracts.pkl')


def clean_doe_grant_data():
    print 'Generating DOE Grant data...'
    data0 = pd.read_excel('../data/doe_grants/2017.xlsx')
    data = pd.read_excel('../data/doe_grants/2016.xlsx')
    data2 = pd.read_excel('../data/doe_grants/2015.xlsx',
                          sheet_name='DOE SC Awards FY 2015')
    data3 = pd.read_excel('../data/doe_grants/2014.xlsx',
                          sheet_name='DOE SC Awards FY 2014')
    data4 = pd.read_excel('../data/doe_grants/2013.xlsx',
                          sheet_name='DOE SC Awards FY 2013', skiprows=1)
    data5 = pd.read_excel('../data/doe_grants/2012.xlsx',
                          sheet_name='DOE SC Awards FY 2012')

    ### FIXES TO RAW DATA
    data2.loc[data2['Institution'] == 'University of Minnesota', 'Congressional District'] = 'MN-05'
    data4.loc[data4['Institution'] == 'CALIFORNIA INST. OF TECHNOLOGY', 'Congressional District *'] = 'CA-27'
    data3.loc[data3['Institution'] == 'California Institute of Technology (CalTech)', 'Congressional District'] = 'CA-27'
    data2.loc[data2['Institution'] == 'California Institute of Technology', 'Congressional District'] = 'CA-27'
    data.loc[data['Institution'] == 'California Institute of Technology', 'Congressional District'] = 'CA-27'
    data0.loc[data0['Institution'] == 'California Institute of Technology', 'Congressional District'] = 'CA-27'
    ### END FIXES

    institutions = pd.concat([data0['Institution'], data['Institution'], data2['Institution'],
                              data3['Institution'], data4['Institution'], data5['Institution']], ignore_index=True, axis=0)
    districts = pd.concat([data0['Congressional District'], data['Congressional District'], data2['Congressional District'],
                           data3['Congressional District'], data4['Congressional District *'], data5['Congressional District']], ignore_index=True, axis=0)
    amounts = pd.concat([data0['Awarded Amount'], data['Awarded Amount'], data2['Awarded Amount'],
                         data3['Awarded Amount'], data4['FY 2013 Funding'], data5['2012 Funding']], ignore_index=True, axis=0)
    years = pd.Series(np.concatenate([2017 * np.ones(len(data0)), 2016 * np.ones(len(data)), 2015 * np.ones(
        len(data2)), 2014 * np.ones(len(data3)), 2013 * np.ones(len(data4)), 2012 * np.ones(len(data5))]))
    states = pd.concat([data0['State'], data['State/Territory'], data2['State/Territory'],
                        data3['State'], data4['State'], data5['State']], ignore_index=True, axis=0)
    programs = pd.concat([data0['Organization'], data['Organization'], data2['Organization'],
                          data3['Organization'], data4['SC Program'], data5['SC Program']], ignore_index=True, axis=0)
    fulldata = pd.concat([programs, years, states, districts, institutions, amounts], axis=1, keys=[
                         'SC Office', 'Year', 'State', 'District', 'Institution', 'Amount'])

    agencies = fulldata['SC Office'].values
    abbrev_agencies = []
    for entry in list(agencies):
        test = re.split(r"\(|\)", str(entry))
        if len(test) > 1:
            abbrev_agencies.append(test[1])
        else:
            abbrev_agencies.append(test[0])
    fulldata['SC Office'] = abbrev_agencies

    hepdata = fulldata[fulldata['SC Office'] == 'HEP']
    hepdata.to_pickle('../cleaned_data/hep_grants.pkl')


def clean_nsf_grant_data():
    print 'Generating NSF Grant data...'
    data2017 = pd.read_csv(
        '../data/nsf_grants/datafeeds\\2017_NSF_Grants_Full_20170915.csv')
    data2016 = pd.read_csv(
        '../data/nsf_grants/datafeeds\\2016_NSF_Grants_Full_20161215.csv')
    data2015 = pd.read_csv(
        '../data/nsf_grants/datafeeds\\2015_NSF_Grants_Full_20151115.csv')
    data2014 = pd.read_csv(
        '../data/nsf_grants/datafeeds\\2014_NSF_Grants_Full_20150515.csv')
    data2013 = pd.read_csv(
        '../data/nsf_grants/datafeeds\\2013_NSF_Grants_Full_20150515.csv')
    data2012 = pd.read_csv(
        '../data/nsf_grants/datafeeds\\2012_NSF_Grants_Full_20150515.csv')
    fulldata = pd.concat([data2017, data2016, data2015,
                          data2014, data2013, data2012])
    mps_grants = fulldata[(fulldata['cfda_program_title'] == 'Mathematical and Physical Sciences') | (
        fulldata['cfda_program_title'] == 'Mathematical and Physical Sciences                                        ')]
    mps_grants = mps_grants.dropna(subset=['principal_place_cd'])

    strlist = []
    for code in mps_grants['principal_place_cd'].values:
        if code == 'ZZ':
            code = '00'
        if len(str(int(code))) < 2:
            strlist.append('0' + str(int(code)))
        else:
            strlist.append(str(int(code)))

    mps_grants['cong_dist'] = mps_grants['principal_place_state_code'] + strlist
    pd.to_pickle(mps_grants, '../cleaned_data/nsf_mps_grants.pkl')


def clean_legislator_data():
    print 'Generating legislator data...'
    data = yaml.load(open('../data/legislator_info/legislators-current.yaml'))
    fullnames = []
    districts = []
    parties = []
    states = []
    bioguides = []
    for member in data:
        fullnames.append(member['name']['official_full'])

        if 'district' in member['terms'][-1].keys():
            districts.append(member['terms'][-1]['state'] + '-' +
                             str(member['terms'][-1]['district']).zfill(2))
        else:
            districts.append(member['terms'][-1]['state'] +
                             '-' + member['terms'][-1]['state'])

        if member['terms'][-1]['party'] == 'Republican':
            parties.append('R')
        elif member['terms'][-1]['party'] == 'Democrat':
            parties.append('D')
        else:
            parties.append('I')

        states.append(member['terms'][-1]['state'])

        bioguides.append(member['id']['bioguide'])

    df = pd.DataFrame([fullnames, districts, parties, states, bioguides])
    df = df.T
    df.to_pickle('../cleaned_data/legislator_key_info.pkl')


def clean_committee_data():
    print 'Generating committee membership data...'
    committees = yaml.load(
        open('../data/legislator_info/committees-current.yaml'))
    members = yaml.load(
        open('../data/legislator_info/committee-membership-current.yaml'))

    df = pd.DataFrame()
    comm_names = {'SSAP16': 'Senate Appropriations Subcommittee on Commerce, Justice, Science, and Related Agencies',
                  'SSAP22': 'Senate Appropriations Subcommittee on Energy and Water Development',
                  'HSAP': 'House Committee on Appropriations',
                  'HSAP10': 'House Appropriations Subcommittee on Energy and Water Development',
                  'HSAP19': 'House Appropriations Subcommittee on Commerce, Justice, and Science',
                  'HSED13': 'House Subcommittee on Higher Education and Workforce Development',
                  'HSED14': 'House Subcommittee on Early Childhood, Elementary, and Secondary Education',
                  'SSAP': 'Senate Committee on Appropriations',
                  'HSIF': 'House Committee on Energy and Commerce',
                  'HSSY': 'House Committee on Science, Space, and Technology',
                  'SSCM': 'Senate Committee on Commerce, Science, and Transportation',
                  'SSEG': 'Senate Committee on Energy and Natural Resources',
                  'SSEG01': 'Senate Energy Subcommittee on Energy',
                  'SSCM24': 'Senate Commerce Subcommittee on Science and Space',
                  'HSSY15': 'House Committee on Science, Space, and Technology; Subcommittee on Research and Technology',
                  'HSSY20': 'House Committee on Science, Space, and Technology; Subcommittee on Energy'}

    for comm in comm_names.keys():
        for mem in members[comm]:
            if mem['party'] == 'majority':
                party = 'Republican'
            else:
                party = 'Democrat'
            ser = pd.Series([mem['name'], str(mem['rank']),
                             party, comm_names[comm], mem['bioguide']])
            df = df.append(ser, ignore_index=True)
            
    df.to_pickle('../cleaned_data/committee_memberships.pkl')
            
if __name__ == '__main__':
    clean_doe_contract_data()
    clean_doe_grant_data()
    clean_nsf_grant_data()
    clean_legislator_data()
    clean_committee_data()