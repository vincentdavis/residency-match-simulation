import sys
import random as r
from applicant import Applicant
from institution import Institution
from importdata import InstitutionData
from match import Match
from results import StatsAndplots

sys.path.append('/Users/vmd/Dropbox/Match/rms')

print('Make a list of Applicants')
all_applicants = []
for x in range(1, 5000):
    tname = Applicant()
    tname.name = str(x)
    ##### Comment out the Following to use defualt
    tname.quality = max(min(r.gauss(50, 20), 100), 1) # on a scale 0-100
    tname.observe_1 = r.gauss(1, .3) # as a percentage, Applicant error in observing the institutions quality
    tname.observe_2 = (r.gauss(1, .3) - tname.observe_1)
    tname.observed_1 = r.gauss(1, .3) # as a percentage, Institutions error "as seen" in observing the applicants quality
    tname.observed_2 = (r.gauss(1, .3) - tname.observed_1) # CORRECT change to observed_1 after interview default = 1
    tname.applied_to_range = [.25, 1.75] # as a percentage, for example [0.8, 1.2]
    tname.num_applied_to = 12 # the maximum number that the applicant applies to
    tname.verbose = True
    all_applicants.append(tname) #Add Applicant to the list of Applicants
print(('number of applicants', len(all_applicants)))

print('Import institution match data for 2008')
data2008 = InstitutionData('/Users/vmd/Dropbox/Match/rms/data/matchdata2008.csv', 140, 'C', 1)
data2008.read_data_file()
data2008.prep_data()
data2008.select_data()

print('Setting Institution Attributes')
all_institutions = []
for x in data2008.finaldata:
    if x[6] > 0:
        tname = Institution() # the Code is set as the object instance name
        tname.name = str(x[1]) #The name attribute is also set as the Code
        tname.openings = x[6] #Set the number of openings, comes from quota in the data file
        tname.prog_type = x[4] #Set the Type, for example 'C' is categorical
        tname.specialty = x[3] #Set the specialty, for example 140 is internal medicine
        tname.institution = x[2] #Set the institution number, basicly the name without the prog_type and specialty info
        tname.specialty_name = x[0] #This is the Speacialty name rather then code
        
        tname.obs_match = x[7] # The is the number that matched in the actual data set
        
        tname.quality = max(min(r.gauss(50, 30), 100), 1)
        tname.number_to_interview = 10 * tname.openings
        tname.observe_1 = r.gauss(1, .3)
        tname.observe_2 = tname.observe_2 = (r.gauss(1, .1)- tname.observe_1)
        tname.observed_1 = r.gauss(1, .3)
        tname.observed_2 = (r.gauss(1, .1)- tname.observed_1) # based on applicant interviewed, percentage
        tname.num_to_rank = 7 * tname.openings
        tname.accept_range = [.7, None] # as a % [.5, 1.5] if [.7, None] then there is no upper limit
    
        all_institutions.append(tname) #add this instance to the list of Intitutions

print('Applicants choose institutions to apply to')
for index, app in enumerate(all_applicants):
    app.apply_list(all_institutions)
    s1 = sum([x.quality for x in app.applied_to])
    assert len(app.applied_to) != 0, 'Applicant must apply to at lest 1 insitution'

print('Institutions invite applicants for interview')
for index, inst in enumerate(all_institutions):
    inst.interview(inst.applied)
    s1 = sum([x.quality for x in inst.invite_interview])
    assert len(inst.invite_interview)<=inst.number_to_interview
    print 'Institution '+ str(inst.name) + ' invited '+str(len(inst.invite_interview))+' to interview '+str(inst.quality)


print('Applicants review the places they interviewed at, and choose who to rank, Then Rank them')
for app in all_applicants:
    print('app.interviewed_at'+str([inst.name for inst in app.interviewed_at]))
    app.rank_interviewed_inst(app.interviewed_at)
    app.sort_rank_interviewed_inst()
    assert len(app.rank_inst) != 0 or app.failed_to_match, 'It should not be that len(app.rank_inst) == 0'+str(app.name)


print('Institutions review applicants after interview, Rank Applicants')
for inst in all_institutions:
    print(str(inst.name) + ' is interviewing '+str(len(inst.invite_interview))+' Applicants')
    inst.inst_rank_app(inst.invite_interview)
    print(str(inst.name) + ' is Ranking '+str(len(inst.rank_list))+' Applicants')
    #print [x.quality for x in inst.rank_list]
    
    
print('Now for the Match')
m1 = Match(all_applicants, all_institutions)
m1.run_match()

print('Results')
r1 = StatsAndplots(all_applicants, all_institutions)
r1.stats()
