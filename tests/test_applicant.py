import unittest
from applicant import Applicant as App
from institution import Institution as Inst

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


class TestApplicant(unittest.TestCase):

    def test_apply_list1(self):
        """Setup 1: number to apply to = number in desired range
        """
        app = App()
        app.quality = 50
        app.num_applied_to = 5
        app.applied_to_range = [.4, 1.2]
        app.apply_list(setup_inst())
        desired = {'i30', 'i40', 'i50', 'i60', 'i70'}
        actual = set([inst.name for inst in app.applied_to])
        self.assertEqual(desired, actual,
                         'desired '+str(desired)+' != '+ 'Actual '+str(actual))

    def test_apply_list2(self):
        '''Setup 2: number to apply to > number in desired range
        range will be expanded
        '''
        app = App()
        app.quality = 50
        app.num_applied_to = 5
        app.observe = 1
        app.applied_to_range = [.8, 1.2]
        app.apply_list(setup_inst())
        desired = set(['i50', 'i60', 'i70', 'i80'])
        actual = set([inst.name for inst in app.applied_to])
        self.assertEqual(desired, actual,
                         'desired '+str(desired)+' != '+ 'Actual '+str(actual))

    def test_apply_list3(self):
        """Setup 3: number to apply to < number in desired range.
        This may be ambiguous becuase the institutions ar randomly selected from
        the list if larger than the number that will be applied to.
        """
        app = App()
        app.quality = 50
        app.num_applied_to = 3
        app.observe = 1
        app.applied_to_range = [.5, 1.5]
        app.apply_list(setup_inst())
        desired = {'i40', 'i50', 'i60'}
        actual = set([inst.name for inst in app.applied_to])
        self.assertEqual(len(desired), len(actual),
                         'desired '+str(len(desired))+' != '+ 'Actual '+str(len(actual)))


    def test_rank_interviewed_inst(self):
        """Select institions that will be ranked"""
        app=App()
        app.quality = 50
        app.num_applied_to = 5
        app.observe = 1
        app.applied_to_range = [.4, 1.2]
        app.apply_list(setup_inst())
        desired = {'i30','i40', 'i50', 'i60', 'i70'}
        actual = set([inst.name for inst in app.applied_to])
        self.assertEqual(actual, desired)


    def test_sort_rank_interviewed_inst(self):
        """Test the sorting of institutions for the rank"""
        app = App()
        app.rank_inst = setup_inst()    #List of institutions that will be sorted "Ranked"
        app.sort_rank_interviewed_inst()
        desired = ['i100', 'i90', 'i80', 'i70', 'i60', 'i50', 'i40', 'i30', 'i20', 'i10']
        actual = [inst.name for inst in app.rank_inst]
        self.assertEqual(actual, desired)

if __name__ == "__main__":
    unittest.main()