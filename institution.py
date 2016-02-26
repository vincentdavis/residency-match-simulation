import random as r


class Institution(object):
    """
    
    Initial Conditions
    ------------------
    quality: Scaler, This is the "true" quality of the institution.
             Defualt: max(min(r.gauss(50, 30), 100), 1)
    openings = Scaler, Numer of openings the institution has to fill or accept
               Defualt: 50 
    number_to_interview: Scaler, Number of Applicants the institution will 
                         interview. It is possible that fewer than this limit 
                         apply and therefore the insitution will (must) 
                         interview less.
                        Default: 10 * self.openings
    observe_1: Scaler, Pre interview observed applicant quality bias.
               Defualt: 1
    observe_2: Scaler, Post interview observed applicant quality bias.
               Defualt: 1
    observed_1: Scaler, Pre interview observed insitution quality bias.
                Defualt: 1
    observed_2: Scaler, Post interview observed intitution quality bias.
                Defualt: 1
    num_to_rank: Scaler, The number of applicants the institution will attempt 
                 to rank. The institution  is limited bt the number that interview.
                 Default: 7 * self.openings
    accept_range, List[], This is the observed applicant quality range that the 
                  institution is willing to interview and rank. This can maybe 
                  during the match to attain the interview and rank number desired
                  Defualt: [.5, 1000]
    
    Apply, Interview, Rank
    ----------------------
    applied: list[] of applicants that applied
    reject_applicant: List[] Rejected applicants, do not interview.
    invite_interview: List[] Invited applicants to interview.
    rank_list: List[] of applicants ranked, index position 0 highest, 400 low.
    
    During Match
    ------------
    matched_to: List[] of applicants that have matched to the institution.
    bumped_applicants: List[] of applicants that where bumped from the institution.
    ranked_to_low: List[] Applicant attmpted to match but was rejected.
    
    Stats
    -----
    
    """

    def __init__(self):
        # Defualt initilazation values
        self.quality = None
        self.openings = None
        self.number_to_interview = None
        self.observe_1 = None
        self.observe_2 = None
        self.observed_1 = None
        self.observed_2 = None
        self.num_to_rank = None
        # self.obs_at_apply = lambda app: (apps_to_rank[app].quality * apps_to_rank[app].observed_1 * self.observe_1)
        # self.obs_at_rank = lambda app: (apps_to_rank[app].quality * apps_to_rank[app].observed_1 * apps_to_rank[app].observed_2 * self.observe_1 *self.observe_2)
        self.applied = []  # list of applicants that applied
        self.reject_applicant = []  # Rejected applicant, do not interview.
        self.invite_interview = []  # Invite applicant to interview.
        self.rank_list = []  # List of applicants ranked, 0 highest, 400 low
        self.matched_to = []  # List of applicants that have matched to the institution
        self.bumped_applicants = []  # List of applicants that where bumped from the institution
        # TODO: how does this get filled,ranked_to_low
        self.ranked_to_low = []

    # This section are some usefull values/calculations

    def Matched_to_count(self):
        """The number of applicats that have matched to the institution"""
        return len(self.matched_to)

    def Space_avalible(self):
        """Are there still empty spots avalible at the institution"""
        return self.openings - len(self.matched_to)

    def Apps_still_can_try(self):
        """This is the list of applicats that have not been proposed in the
        match proccess to the institution"""
        return [x for x in self.rank_list if x not in self.matched_to and x not in self.bumped_applicants and x not in self.ranked_to_low]

    def Lowest_rank(self):
        """finds the lowest ranked applicatn that is currently matched,returns the applicant and the rank"""
        rank = max([self.rank_list.index(x) for x in self.matched_to])
        app = self.rank_list[rank]
        return [rank, app]

    def Get_applicant_rank(self, app):
        """ calculates the applicants rank"""
        return self.rank_list.index(app)

    def _Bump_applicant(self, app):
        """Bumps an applicant that was matched, send message back to applicant instance"""
        self.matched_to.remove(app)
        self.bumped_applicants.append(app)

    def _Preinterview_sort(self, applist):
        """Preinterview sorting of applicants"""
        preinterview = lambda app: (app.quality * app.observed_1 * self.observe_1)
        applist.sort(key=preinterview, reverse=1)
        # return applist

    def _Postinterview_sort(self, applist):
        """Preinterview sorting of applicants"""
        try:
            postinterview = lambda app: (app.quality * app.observed_1 * app.observed_2 * self.observe_1 * self.observe_2)
        except Exception as e:
            print(e)
            print('Values are {}, {}, {}, {}, {}'.format(app.quality * app.observed_1 * app.observed_2 * self.observe_1 * self.observe_2))
            raise
        applist.sort(key=postinterview, reverse=1)
        # return applist

    def interview(self, applist):
        """
        The first condition is to interview as many as they wish to
        (number_to_interview). If more than that apply then they do not invite
        the least qualified applicants. Invites are based on applicant.observe_1
        """
        if len(applist) <= self.number_to_interview:  # Has the insitution recieved to many interview requests
            self.invite_interview = applist[:]  # interview all that applied
        else:
            self._Preinterview_sort(applist)  # sort the applicant list.
            self.invite_interview = applist[0:self.number_to_interview]  # take the best from the sorted applicant list
            self.reject_applicant = applist[self.number_to_interview:]
        assert ((len(self.invite_interview) + len(self.reject_applicant)) ==
                len(applist)), '# applicants = number interview+number rejected'
        for app in self.invite_interview:
            app.interviewed_at.append(self)

    def inst_rank_app(self, apps_to_rank):
        """
        Sorts the list of applicants.
        This is then the rank order.
        There is no strategy always rank by observed quality.
        """
        self._Postinterview_sort(apps_to_rank)
        # TODO: need to filter the list based on self.accept_range
        # filter((self.observer_at_rank(apps_to_rank[x])) <= self.accept_range[0])
        self.rank_list = apps_to_rank

    def Proposed_applicant(self, applicant):
        """Test's Proposed applicant to see if they match, if so update
        insitution. Return results"""
        app_matched = None
        app_to_bump = None
        # These lines are to help catch errors
        assert applicant in self.Apps_still_can_try(), \
            'Applicant ' + str(applicant.name) + ' not in the list of still can try'
        assert (self.Space_avalible() > 0 or
                self.Lowest_rank()[0] > self.Get_applicant_rank(applicant) or
                self.Lowest_rank()[0] < self.Get_applicant_rank(applicant)), \
            'Proposed_applicant error'
        if self.Space_avalible() > 0:  # The institution has not yet filled.
            app_matched = True
            applicant.matched_to = self
        elif self.Lowest_rank()[0] > self.Get_applicant_rank(applicant):  # Applicant can bump the lowest matched applicant
            app_matched = True
            app_to_bump = self.Lowest_rank()[1]
            self._Bump_applicant(app_to_bump)
            applicant.matched_to = self
            assert app_to_bump not in self.matched_to, 'app_to_bump not in self.matched_to'
            assert app_to_bump in self.bumped_applicants, 'app_to_bump in self.bumped_applicants'
        else:  # Applicant fails to match at institution
            assert self.Lowest_rank()[0] < self.Get_applicant_rank(applicant)
            app_matched = False
            self.ranked_to_low.append(applicant)
            applicant.not_matched_to.append(self)

        return [app_matched, app_to_bump]
