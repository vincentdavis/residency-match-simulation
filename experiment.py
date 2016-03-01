from models import *

def create_applicants(applicant):
    count = 5000
    for a in range(5000):
        app = applicant.create(name=A+str(a+1), quality=(100/count)*(a+1),
                               apply=1, visit=1, marketing=1, applylimit=100)

def create_intitution(institution):
    count = 100
    for a in range(5000):
        app = institution.create(name=I+str(a+1), quality=(100/count)*(a+1),
                               application=1, interview=1, marketing=1, interviewlimit=5000)


def request_interview(self):
    pass

def invite_interview (self):
    pass

def rank_inst(self):
    pass

def rank_app(self):
    pass

if __name__ == "__main__":
    database.connect()
    try:
        database.create_tables([Applicant, Institution, Match])
    except:
        import os
        os.remove('match.db')
        database.create_tables([Applicant, Institution, Match])
    create_applicants(Applicant)
    create_intitution(Institution)