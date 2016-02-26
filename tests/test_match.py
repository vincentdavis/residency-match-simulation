import unittest
from applicant import Applicant as App
from institution import Institution as Inst
from match import Match

def setup_app():
    applist=[]
    for qualty in [100,20,90,80,50,30,40,10,70,60, 25,95,85,55,35, 45, 15, 75, 65, 15, 10, 5, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        name = App()
        name.quality = qualty
        name.observed_1 = .8
        name.observed_2 = 1.25
        name.applied_to = 3
        name.name = 'a'+str(qualty)
        applist.append(name)
    return applist

def setup_inst():
    instlist =[]
    for qualty in [100,20,90,80,50,30,40,10,70,60]:
        name = Inst()
        name.quality = qualty
        name.observed_1 = .8
        name.observed_2 = 1.25
        name.number_to_interview = 5
        name.openings = 2
        name.name = 'i'+str(qualty)
        instlist.append(name)
    return instlist

class TestMatch(unittest.TestCase):
    
    def test_Applicant_not_matched(self):
        amatch=Match(setup_app(), setup_inst()).Applicant_not_matched()
        self.assertEqual(amatch, 1, [i.name for i in amatch])
        
        
    def test_run_match(self):
        amatch=Match(setup_app(), setup_inst())
        self.assertEqual(amatch, 1, [i.name for i in amatch.app_list])
if __name__ == "__main__":
    unittest.main()