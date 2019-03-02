import re
import numpy as np
import pandas as pd
import yaml
from glob import glob
import requests
import os
import zipfile

def download_latest_data(currentFY,n_years_desired):

    #find latest datestamp on usaspending files
    usaspending_base = 'https://files.usaspending.gov/award_data_archive/'
    save_path = '../new_data/'
    r = requests.get(usaspending_base, allow_redirects=True)
    r.raise_for_status()
    datestr = re.findall('_(\d{8}).zip',r.content)[0]

    for FY in np.arange(currentFY-n_years_desired+1,currentFY+1):
        doe_contracts_url = usaspending_base+str(FY)+'_089_Contracts_Full_' + datestr + '.zip'
        doe_grants_url = usaspending_base+str(FY)+'_089_Assistance_Full_' + datestr + '.zip'
        nsf_grants_url = usaspending_base+str(FY)+'_049_Assistance_Full_' + datestr + '.zip'
        doe_sc_url = 'https://science.energy.gov/~/media/_/excel/universities/DOE-SC_Grants_FY'+str(FY)+'.xlsx'

        for url in [doe_contracts_url,doe_grants_url,nsf_grants_url,doe_sc_url]:

            filename = url.split('/')[-1]
            if os.path.exists(save_path+filename): continue

            if url == doe_sc_url: 
                verify='doe_cert.pem'
            else:
                verify=True

            try: 
                r = requests.get(url, allow_redirects=True,verify=False)
                r.raise_for_status()
            except:
                print 'could not find', url
                continue

            # DOE website stupidly returns a 200 HTTP code when displaying 404 page :/
            page_not_found_text = 'The page that you have requested was not found.'
            if page_not_found_text in r.content: 
                print 'could not find', url
                continue

            open(save_path+filename, 'wb+').write(r.content)
    print 'Data download complete'
    
def unzip_all():
    for unzip_this in glob('../new_data/*.zip'):
        zipper = zipfile.ZipFile(unzip_this,'r')
        zipper.extractall(path='../new_data')
    
def clean_doe_contract_data():
    print 'Generating DOE Contract data...'

    contract_file_list = glob('../new_data/*089_Contracts*.csv')
    contract_df_list = []
    for contract_file in contract_file_list:
        df = pd.read_csv(contract_file)
        df['Year'] = contract_file.split('/')[-1][:4]
        contract_df_list.append(df)
    fulldata = pd.concat(contract_df_list,ignore_index=True)

    sc_awarding_offices = ['CHICAGO SERVICE CENTER (OFFICE OF SCIENCE)',
                  'OAK RIDGE OFFICE (OFFICE OF SCIENCE)',
                  'SC CHICAGO SERVICE CENTER',
                  'SC OAK RIDGE OFFICE']

    sc_funding_offices = ['CHICAGO SERVICE CENTER (OFFICE OF SCIENCE)',
                          'OAK RIDGE OFFICE (OFFICE OF SCIENCE)',
                          'SCIENCE',
                          'SC OAK RIDGE OFFICE',
                          'SC CHICAGO SERVICE CENTER'
                         ]

    sc_contracts = fulldata[(fulldata['awarding_office_name'].isin(
        sc_awarding_offices)) | (fulldata['funding_office_name'].isin(sc_funding_offices))]

    #Clean data
    
    sc_contracts = sc_contracts[['award_id_piid', 'federal_action_obligation','recipient_name',
                                 'primary_place_of_performance_state_code',
                                 'primary_place_of_performance_congressional_district',
                                 'product_or_service_code_description',
                                 'Year'
                                 ]]
    
    sc_contracts = sc_contracts.rename(columns = {
        'federal_action_obligation':'Amount ($)',
        'award_id_piid' : 'award_id',
        'recipient_name' : 'Vendor',
        'primary_place_of_performance_state_code' : 'State',
        'primary_place_of_performance_congressional_district' : 'District',
        'product_or_service_code_description' : 'Item'
    })
    
    sc_contracts = sc_contracts.dropna(subset=['District'])
    sc_contracts['District'] = sc_contracts['State'] + sc_contracts['District'].map(int).map(str).str.zfill(2)
    sc_contracts['Amount ($)'] = sc_contracts['Amount ($)'].map(int)
    
    sc_contracts.to_pickle('../new_data/cleaned/sc_contracts.pkl')


def clean_doe_grant_data():
    print 'Generating DOE Grant data...'
    dataA = pd.read_excel('../new_data/DOE-SC_Grants_FY2018.xlsx')
    data0 = pd.read_excel('../new_data/DOE-SC_Grants_FY2017.xlsx')
    data = pd.read_excel('../new_data/DOE-SC_Grants_FY2016.xlsx')
    data2 = pd.read_excel('../new_data/DOE-SC_Grants_FY2015.xlsx',
                          sheet_name='DOE SC Awards FY 2015')
    data3 = pd.read_excel('../new_data/DOE-SC_Grants_FY2014.xlsx',
                          sheet_name='DOE SC Awards FY 2014')
    data4 = pd.read_excel('../new_data/DOE-SC_Grants_FY2013.xlsx',
                          sheet_name='DOE SC Awards FY 2013', skiprows=1)
    data5 = pd.read_excel('../new_data/DOE-SC_Grants_FY2012.xlsx',
                          sheet_name='DOE SC Awards FY 2012')

    ### FIXES TO RAW DATA
    data2.loc[data2['Institution'] == 'University of Minnesota', 'Congressional District'] = 'MN-05'
    data4.loc[data4['Institution'] == 'CALIFORNIA INST. OF TECHNOLOGY', 'Congressional District *'] = 'CA-27'
    data3.loc[data3['Institution'] == 'California Institute of Technology (CalTech)', 'Congressional District'] = 'CA-27'
    data2.loc[data2['Institution'] == 'California Institute of Technology', 'Congressional District'] = 'CA-27'
    data.loc[data['Institution'] == 'California Institute of Technology', 'Congressional District'] = 'CA-27'
    data0.loc[data0['Institution'] == 'California Institute of Technology', 'Congressional District'] = 'CA-27'
    ### END FIXES

    institutions = pd.concat([dataA['Institution'],data0['Institution'], data['Institution'], data2['Institution'],
                              data3['Institution'], data4['Institution'], data5['Institution']], ignore_index=True, axis=0)
    districts = pd.concat([dataA['Congressional District'],data0['Congressional District'], data['Congressional District'], data2['Congressional District'],
                           data3['Congressional District'], data4['Congressional District *'], data5['Congressional District']], ignore_index=True, axis=0)
    amounts = pd.concat([dataA['Awarded Amount'],data0['Awarded Amount'], data['Awarded Amount'], data2['Awarded Amount'],
                         data3['Awarded Amount'], data4['FY 2013 Funding'], data5['2012 Funding']], ignore_index=True, axis=0)
    years = pd.Series(np.concatenate([2018 * np.ones(len(dataA),dtype=int), 2017 * np.ones(len(data0),dtype=int), 2016 * np.ones(len(data),dtype=int), 2015 * np.ones(
        len(data2),dtype=int), 2014 * np.ones(len(data3),dtype=int), 2013 * np.ones(len(data4),dtype=int), 2012 * np.ones(len(data5),dtype=int)]))
    states = pd.concat([dataA['State'], data0['State'], data['State/Territory'], data2['State/Territory'],
                        data3['State'], data4['State'], data5['State']], ignore_index=True, axis=0)
    programs = pd.concat([dataA['Program Office'], data0['Organization'], data['Organization'], data2['Organization'],
                          data3['Organization'], data4['SC Program'], data5['SC Program']], ignore_index=True, axis=0)
    fulldata = pd.concat([programs, years, states, districts, institutions, amounts], axis=1, keys=[
                         'SC Office', 'Year', 'State', 'District', 'Institution', 'Amount ($)'])

    fulldata['State'] = fulldata['State'].map(str).map(str.strip)
    
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
    hepdata = hepdata.dropna(subset=['Amount ($)'])
    hepdata['Amount ($)'] = hepdata['Amount ($)'].map(int)
    
    hepdata.to_pickle('../new_data/cleaned/hep_grants.pkl')


def clean_nsf_grant_data():
    print 'Generating NSF Grant data...'

    contract_file_list = glob('../new_data/*049_Assistance*.csv')
    contract_df_list = []
    for contract_file in contract_file_list:
        df = pd.read_csv(contract_file)
        df['Year'] = contract_file.split('/')[-1][:4]
        contract_df_list.append(df)
    fulldata = pd.concat(contract_df_list,ignore_index=True)
    
    mps_grants = fulldata[fulldata['cfda_title'].map(str.strip).map(str.lower) == 'mathematical and physical sciences']
    
    mps_grants = mps_grants[['Year','cfda_title','federal_action_obligation',
                            'recipient_state_code', 'recipient_congressional_district',
                             'recipient_name'
                            ]]
    
    mps_grants = mps_grants.rename(columns = {
        'federal_action_obligation' : 'Amount ($)',
        'recipient_state_code' : 'State',
        'recipient_congressional_district' : 'District',
        'recipient_name' : 'Institution'
    })
    
    mps_grants = mps_grants.dropna(subset=['District'])

    mps_grants['District'] = mps_grants['State'] + mps_grants['District'].map(int).map(str).str.zfill(2)
    mps_grants.loc[mps_grants['District'] == 'OR00', 'State'] = 'PR'
    mps_grants.loc[mps_grants['District'] == 'OR00', 'District'] = 'PR00'
    
    mps_grants['Amount ($)'] = mps_grants['Amount ($)'].map(int)
    pd.to_pickle(mps_grants, '../new_data/cleaned/nsf_mps_grants.pkl')


def clean_legislator_data():
    print 'Generating legislator data...'
    data = yaml.load(open('../../congress-legislators/legislators-current.yaml'))
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
    df.to_pickle('../new_data/cleaned/legislator_key_info.pkl')


def clean_committee_data():
    try:
        legislators = pd.read_pickle('../new_data/cleaned/legislator_key_info.pkl')
    except:
        print 'Run clean_legislator_data() first!'
        return
    print 'Generating committee membership data...'
    committees = yaml.load(
        open('../../congress-legislators/committees-current.yaml'))
    members = yaml.load(
        open('../../congress-legislators/committee-membership-current.yaml'))

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
                  #'SSCM24': 'Senate Commerce Subcommittee on Science and Space',
                  'HSSY15': 'House Committee on Science, Space, and Technology; Subcommittee on Research and Technology',
                  'HSSY20': 'House Committee on Science, Space, and Technology; Subcommittee on Energy'}

    for comm in comm_names.keys():
        for mem in members[comm]:
            party_abbr = legislators[legislators[4] == mem['bioguide']][2].values[0] #pick out party code, make it not a list
            if party_abbr == 'D':
                party = 'Democrat'
            elif party_abbr == 'R':
                party = 'Republican'
            else:
                party = 'Independent'
            ser = pd.Series([mem['name'], str(mem['rank']),
                             party, comm_names[comm], mem['bioguide']])
            df = df.append(ser, ignore_index=True)
            
    df.to_pickle('../new_data/cleaned/committee_memberships.pkl')
            
if __name__ == '__main__':
    if not os.path.exists('../new_data/cleaned'): os.makedirs('../new_data/cleaned')
    download_latest_data(2019,8)
    unzip_all()
    clean_doe_contract_data()
    clean_doe_grant_data()
    clean_nsf_grant_data()
    clean_legislator_data()
    clean_committee_data()
