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
        count = 50
        for a in range(count):
            app = applicant.create(name='A'+str(a+1), quality=(100/count)*(a+1),
                                   apply=1, visit=1, marketing=1, applylimit=100)

    def create_intitution(institution):
        count = 10
        for a in range(count):
            app = institution.create(name='I'+str(a+1), quality=(100/count)*(a+1),
                                   application=1, interview=1, marketing=1, interviewlimit=5000)

    def request_interview(applicant, institution):
        for a in applicant:
            for i in institution:
                Match.create(inst=i, app=a, req_interview=1, matched=-1)

    def invite_interview (match):
        for m in match:
            if m.req_interview==1: # this should be everyone.
                m.inst_interview = 1
                m.save()

    def rank_inst(match, institution, applicant):
        applist = []
        for i in institution:
            for m in match.select().where(match.inst == i):
                #print('Name: {} , Quality: {}'.format(applicant.name), str(applicant.quality))
                applist.append(applicant.get(applicant.id == m.app_id))
                print(applist)








    def rank_app(self):
        pass
    create_applicants(Applicant)
    create_intitution(Institution)
    request_interview(Applicant, Institution)
    invite_interview (Match)
    rank_inst(Match, Institution, Applicant)

