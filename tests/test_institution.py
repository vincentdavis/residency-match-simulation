import unittest
from applicant import Applicant as App
from institution import Institution as Inst

def setup_app():
    applist=[]
    for qualty in [100,20,90,80,50,30,40,10,70,60]:
        name = App()
        name.quality = qualty
        name.observed_1 = .8
        name.observed_2 = 1.25
        name.name = 'a'+str(qualty)
        applist.append(name)
    return applist

class TestInstitution(unittest.TestCase):

    def test_interview(self):
        """
        Interview selection Test 1: , number that apply > number to interview
        """
        inst = Inst()
        inst.quality = 50
        inst.observe_1 = 1
        inst.observe_2 = 1
        inst.number_to_interview = 5
        inst.interview(setup_app())
        desired = set(['foo']) # Need to determin the right answer
        actual = set([app.name for app in inst.invite_interview])
        print('actual 1',actual)
        self.assertEqual(desired, actual,
                         'desired '+str(desired)+' != '+ 'Actual '+str(actual))
#TODO: need to make sure the applicants that interviewed are updated.
    # for app in self.invite_interview: app.interviewed_at.append(self)

    def test_inst_rank_app(self):
        """
        Rank selection Test 1:
        """
        inst = Inst()
        inst.quality = 50
        inst.observe_1 = 1
        inst.observe_2 = 1
        inst.num_to_rank = 5
        inst.accept_range = [.5, 1000]
#TODO: need to filter based on inst.accept_range
        inst.inst_rank_app(setup_app())
        #order matters on rank_list
        desired = ['foo'] # Need to determin the right answer
        actual = [app.name for app in inst.rank_list]
        print('actual 2',actual)
        self.assertEqual(desired, actual,
                         'desired '+str(desired)+' != '+ 'Actual '+str(actual))

    def test_Proposed_applicant_1(self):
        """Proposed_applicant_1: Institution has room (is not filled) accepts
        applicant
        """
        apps = setup_app()
        #setup institution
        inst = Inst()
        inst.matched_to = [apps[5], apps[3]]
        #inst.rank_list = apps Next line takes care of this
        inst.inst_rank_app(apps)
        inst.bumped_applicants = [apps[1]]
        inst.ranked_to_low = []
        inst.openings = 5
        results = inst.Proposed_applicant(apps[6])
        self.assertEqual((results[0] and results[1]==None), True, 
                         'There was room, applicant should have been accepted'+
                         str(results[0]) + ' ' +str(results[1]))
        
    def test_Proposed_applicant_2(self):
        """Proposed_applicant_2: Institution is filled applicant can bump lowest
        ranked applicant
        """
        apps = setup_app()
        #setup institution
        inst = Inst()
        #inst.rank_list = apps Next line takes care of this
        inst.inst_rank_app(apps)
        inst.matched_to = [inst.rank_list[0], inst.rank_list[2], 
                           inst.rank_list[4], inst.rank_list[6]]
        inst.bumped_applicants = [inst.rank_list[9]]
        inst.ranked_to_low = []
        inst.openings = 4
        results = inst.Proposed_applicant(inst.rank_list[1])
        self.assertEqual((results[0] and results[1]==inst.rank_list[6]), True, 
                         'Applicant should have bumped a10 '+
                         str(results[0]) + ' ' +str(results[1].name))
        
    def test_Proposed_applicant_3(self):
        """Proposed_applicant_3: Institution is filled applicant can NOT bump
        """
        apps = setup_app()
        #setup institution
        inst = Inst()
        #inst.rank_list = apps Next line takes care of this
        inst.inst_rank_app(apps)
        inst.matched_to = [inst.rank_list[0], inst.rank_list[1], 
                           inst.rank_list[2], inst.rank_list[3]]
        inst.bumped_applicants = [inst.rank_list[9]]
        inst.ranked_to_low = []
        inst.openings = 4
        results = inst.Proposed_applicant(inst.rank_list[4])
        self.assertEqual((not(results[0]) and results[1]==None), True, 
                         ('Applicant should have matched '+
                         str(results[0]) + ' ' +str(results[1])))

if __name__ == "__main__":
    unittest.main()