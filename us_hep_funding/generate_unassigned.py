import pandas as pd
import numpy as np
import sys
import codecs
from tabulate import tabulate

import generate_webpages


sc_contracts = pd.read_pickle('../new_data/cleaned/sc_contracts.pkl')

start_year = np.min(sc_contracts['Year'])
n_years = len(sc_contracts['Year'].unique())
end_year = int(start_year) + n_years - 1

#DOE HEP grants
grants = pd.read_pickle('../new_data/cleaned/hep_grants.pkl')
grants_by_district = grants.groupby(['District'])
grants_by_state = grants.groupby(['State'])

#NSF MPS Grants
nsf_grants = pd.read_pickle('../new_data/cleaned/nsf_mps_grants.pkl')
nsf_by_state = nsf_grants.groupby(['State'])
nsf_by_district = nsf_grants.groupby(['District'])

#SULI Students
suli_students = pd.read_pickle('../new_data/cleaned/suli_students.pkl')
natlabs = pd.read_csv('../data/national_labs_geocodio.csv')
natlabs = natlabs[['Lab','City','Latitude','Longitude']].dropna()
natlabs = natlabs.rename(columns={'Lab':'Host Lab','City':'Lab City','Latitude':'Lab Latitude','Longitude':'Lab Longitude'})
suli_students = suli_students.merge(natlabs,on='Host Lab')
suli_students_by_state = suli_students.groupby(['State'])
suli_students_by_district = suli_students.groupby(['Congressional District'])


legislators = pd.read_pickle('../new_data/cleaned/legislator_key_info.pkl')
committee_members = pd.read_pickle('../new_data/cleaned/committee_memberships.pkl').groupby(4)

with open('/Users/mbaumer/Documents/current_unassigned.txt','r') as f:
    text = f.read()
    
unclaimed_gop = []
for i in range(100):
    try:
        entry = text.split('badge-danger')[i].split('\n')[1].strip()[2:]
    except IndexError:
        continue
    if 'At-Large' in entry: continue
    if len(entry) == 4:
        entry = entry[:2] + '-0' + entry[-1]
    else:
        entry = entry[:2] + '-' + entry[3:]
    unclaimed_gop.append(entry)
unclaimed_gop = unclaimed_gop[1:]
    
unclaimed_dems = []
for i in range(100):
    try:
        entry = text.split('badge-primary')[i].split('\n')[1].strip()[2:]
    except IndexError:
        continue
    if 'At-Large' in entry: continue
    if len(entry) == 4:
        entry = entry[:2] + '-0' + entry[-1]
    else:
        entry = entry[:2] + '-' + entry[3:]
    unclaimed_dems.append(entry)
unclaimed_dems = unclaimed_dems[1:]

unclaimed = unclaimed_dems + unclaimed_gop

def email_about_district(distcode):
    this_rep = legislators[legislators[1] == distcode]
    try:
        hep = grants_by_district.get_group(distcode)['Amount ($)'].sum()
    except KeyError:
        hep = 0
        pass
    try:
        nsf = nsf_by_district.get_group(distcode[0:2] + distcode[3:])['Amount ($)'].sum()
    except KeyError:
        nsf = 0
        pass
    try:
        sc = sc_contracts.groupby('District').get_group(distcode[0:2] + distcode[3:])['Amount ($)'].sum()
    except KeyError:
        sc = 0
        pass
    try:
        nsuli = suli_students_by_district.get_group(distcode[0:2] + distcode[3:]).count()['Name']
    except KeyError:
        nsuli = 0
        pass
    
    return hep,nsf,sc,nsuli

districts_w_hep = []
districts_nsf = []
districts_sc = []
districts_suli = []
districts_only_suli = []
for current_dist in unclaimed:
    hep,nsf,sc,nsuli = email_about_district(current_dist)

    if hep > 6000:
        districts_w_hep.append([current_dist,hep])
    if (nsf > 0) & (nsuli == 0):
        districts_nsf.append([current_dist,nsf])
    if sc > 0:
        districts_sc.append([current_dist,sc])
    if (nsuli > 0) & (nsf > 0):
        districts_suli.append([current_dist,nsuli])
    if (nsuli > 0) & (nsf <= 0):
        districts_only_suli.append([current_dist,nsuli])
        
import sys
import codecs
f = codecs.open('../docs/unclaimed.md','w','utf-8')
sys.stdout = f
print '---'
print 'title: Unassigned Districts'
print 'layout: page'
print 'permalink: \'/unclaimed/\''
print '---'

print '<style type="text/css">'

print '.alert {'
print '  position: relative;'
print '  padding: 0.75rem 0.75rem;'
print '  border: 1px solid transparent;'
print '  border-radius: 0.25rem;'
print '}'

print '.alert-info {'
print '  color: #fdfdfd;'
print '  background-color: #2a7ae2;'
print '  border-color: #fdfdfd;'
print '}'
print '</style>'

print '<div class="alert alert-info">'
print 'Be sure to mark your chosen district as "claimed" in WHIPS before contacting any offices using this information! List current as of 3/9; 20:24PST'
print '</div>'
print '---'

if len(districts_w_hep) > 0:
    print '### Unclaimed districts with Office of HEP grants'
    print '*Sample text (replace ```XXX``` with district info):* \n'
    print 'In addition to its broader impacts on the economy and national security, HEP research also has local impact in the ```XXX``` District. In recent years, researchers at ```XXX``` have received over $```XXX``` in grants from the Department of Energy Office of High Energy Physics.'
    print '<ol>'
    for dist in districts_w_hep:
        dist = dist[0]
        state = dist[:2].upper()
        print '<li><a href="https://mbaumer.github.io/us_hep_funding/states/'+state+'/#'+dist.upper()+'">'+dist+'</a></li>'
    print '</ol>'
    print '---'

if len(districts_suli) > 0:
    print '### Unclaimed districts with NSF MPS grants **AND** SULI/CCI students'
    print '*Sample text (replace ```XXX``` with district info):* \n'
    print 'In addition to its broader impacts on the economy and national security, HEP research also has local impact in the ```XXX``` District. Researchers at ```XXX``` have received over $```XXX``` in grants from the NSF Directorate for Mathematical and Physical Sciences, which along with the DOE Office of High Energy Physics fund the majority of our research. In addition, ```XXX``` students from ```XXX``` have earned prestigious SULI/CCI research internships at DOE National Laboratories, part of our field\'s wide-ranging efforts to develop technical skills in a new generation of the STEM workforce.'
    print '<ol>'
    for dist in districts_suli:
        dist = dist[0]
        state = dist[:2].upper()
        print '<li><a href="https://mbaumer.github.io/us_hep_funding/states/'+state+'/#'+dist.upper()+'">'+dist+'</a></li>'
    print '</ol>' 
    print '---'

if len(districts_nsf) > 0:
    print '### Unclaimed districts with NSF MPS grants'
    print '*Sample text (replace ```XXX``` with district info):* \n'
    print 'In addition to its broader impacts on the economy and national security, HEP research also has local impact in the ```XXX``` District. Researchers at ```XXX``` have received over $```XXX``` in grants from the NSF Directorate for Mathematical and Physical Sciences, which along with the DOE Office of High Energy Physics fund the majority of our research.'
    print '<ol>'
    for dist in districts_nsf:
        dist = dist[0]
        state = dist[:2].upper()
        print '<li><a href="https://mbaumer.github.io/us_hep_funding/states/'+state+'/#'+dist.upper()+'">'+dist+'</a></li>'
    print '</ol>'   
    print '---'

if len(districts_only_suli) > 0:
    print '### Unclaimed districts with SULI/CCI Students'
    print '*Sample text (replace ```XXX``` with district info):* \n'
    print 'In addition to its broader impacts on the economy and national security, HEP research also has local impact in the ```XXX``` District. In recent years, ```XXX``` students from ```XXX``` have earned prestigious SULI/CCI research internships at DOE National Laboratories, part of our field\'s wide-ranging efforts to develop technical skills in a new generation of the STEM workforce.'
    print '<ol>'
    for dist in districts_only_suli:
        dist = dist[0]
        state = dist[:2].upper()
        print '<li><a href="https://mbaumer.github.io/us_hep_funding/states/'+state+'/#'+dist.upper()+'">'+dist+'</a></li>'
    print '</ol>'
