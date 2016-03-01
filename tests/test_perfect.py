from models import *
from unittest import TestCase

class testperfect_1(TestCase):
    try:
        database.connect()
        database.create_tables([Applicant, Institution, Match])
    except:
        import os
        os.remove('match.db')
        database.connect()
        database.create_tables([Applicant, Institution, Match])

    def create_applicants(applicant):
        count = 5000
        for a in range(5000):
            app = applicant.create(name='A'+str(a+1), quality=(100/count)*(a+1),
                                   apply=1, visit=1, marketing=1, applylimit=100)

    def create_intitution(institution):
        count = 100
        for a in range(5000):
            app = institution.create(name='I'+str(a+1), quality=(100/count)*(a+1),
                                   application=1, interview=1, marketing=1, interviewlimit=5000)

    def request_interview(applicant, institution):
        for a in applicant:
            for i in institution:
                Match.create(inst=i, app=a, matched=-1)


        pass

    def invite_interview (self):
        pass

    def rank_inst(self):
        pass

    def rank_app(self):
        pass
    create_applicants(Applicant)
    create_intitution(Institution)
    request_interview(Applicant, Institution)
