import unittest
from applicant import Applicant as App
from institution import Institution as Inst
from match import Match

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

def setup_inst():
    instlist =[]
    for qualty in [100,20,90,80,50,30,40,10,70,60]:
        name = Inst()
        name.quality = qualty
        name.observed_1 = .8
        name.observed_2 = 1.25
        name.name = 'i'+str(qualty)
        instlist.append(name)
    return instlist

class TestMatch(unittest.TestCase):
    
    def test_Applicant_not_matched(self):
        amatch=Match(setup_app, setup_inst)
        
        
    def test_run_match(self):
        amatch=Match(setup_app, setup_ins)
      
if __name__ == "__main__":
    unittest.main()