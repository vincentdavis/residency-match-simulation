import random as r


class Applicant(object):
    """
    This class represents an applicant and their attributes and decisions.
    All initial conditions attributes have defualt values and each can be specified
    Any attribute can be set.
    
    An Applicant observes the quality of an Institution. The Observed institution 
    quality with respect to the True quality is calculated during 2 phases of the
    simulation.
    1: Determinig which institutions to apply to ,Observed Quality of institution (OQI)
    OQI = intitution.observe_1 * applicant.observe
    2: Determining the ranking of institutions
    OQI = intitution.observe_1 * intitution.observe_2 * applicant.observe
    
    By Defualt all observed bias is set to 1 i.e. no bias true quality is observed
    
    Initial Conditions
    ------------------
    quality : Scaler, This is the "True" quality of the applicants, all observed qualitys
              are relitive to this value.
              Defualt: max(min(r.gauss(50, 20), 100), 1)
    observe : Scaler, Bias of in observing the quality of an institution. Can be a 
              constant or function.
              Defualt: 1 , "no bias"
    observed_1 : Scaler, bias of an observing istitution prior to interview
                 Defualt = 1
    observed_2 : Scaler, Bais of an observing institution after interview and for the rank
                 Defualt = 1
    applied_to_range : list[], Observed institutional quality range an applicant
                       applies to. 
                       Example :  
                       applicant.quality = 50,  
                       applicant.applied_to_range = [.5, 1.5]
                       The the applicant would apply to institutions within and 
                       observed quality of (25, 75).
    num_applied_to: Scaler, This is the number of insitutions an applicant will 
                    apply to. The applied_to_range is over riden by this value. 
                    That is if applied_to_range produces a list of institutions 
                    to small or to bug it is adjusted.
    num_to_rank: Scaler, The applicant will try to rank this number of institutions.
                 There is no garantee that they will interview at this many so it
                 might not be possible.
    
    Apply, Interview, Rank
    ----------------------
    applied_to : List of institutions the applicant applied to
    interviewed_at : List of institutions the applicant interviewd at
    no_interviewed_at : The compliment of interviewed_at with respect to applied_to
    rank_inst : List of institutions the applicant Ranked
    not_rank_inst : List of institutions the applicant chose not to rank
    
    During Match
    ------------
    matched_to : The institution the applicant is matched to. (if matched)
    not_matched_to : List of institutions the applicant failed to match to.
    failed_to_match : True, False
    
    Stats
    -----
    matched_inst_rank : Ther applicants rank of the instituion tha applicant is 
                        matched to
    """

    def __init__(self):
        self.quality = max(min(r.gauss(50, 20), 100), 1)
        self.observe = 1
        self.observed_1 = 1
        self.observed_2 = 1
        self.applied_to_range = [0, 1000]
        self.num_applied_to = 12
        self.num_to_rank = 6
        self.applied_to = []
        self.interviewed_at = []
        self.no_interviewed_at = []
        self.rank_inst = []
        self.not_rank_inst = []
        self.matched_to = None
        self.not_matched_to = []
        self.failed_to_match = False
        self.matched_inst_rank = None
        self.verbose = False

    def Institution_to_try_next(self):
        """Used during match
        If not matched this returns the next insitutions the applicant will be
        proposed to.
        """
        rankl = self.rank_inst[:]
        notmatch = self.not_matched_to[:]
        assert rankl[0:len(notmatch)] == notmatch, 'rankl[0:len(notmatch)] == notmatch'
        if not rankl[len(notmatch):]:
            self.failed_to_match = True
            return None
        else:
            return rankl[len(notmatch):len(notmatch) + 1][0]

    def apply_list(self, instlist):
        """Determin the institutions the applicant will apply to.
        """
        temp = []
        # Lower and upper bounds of institution that will be applied to
        lowerb = self.quality * self.applied_to_range[0]
        upperb = self.quality * self.applied_to_range[1]
        while len(temp) < self.num_applied_to:  # Make sure they apply to at least num_applied_to
            for inst in instlist:
                observed_quality = inst.quality * inst.observed_1 * self.observe  # Don't really need self.observe as it effects all the same
                if (lowerb <= observed_quality) and (observed_quality <= upperb):
                    temp.append(inst)
            if len(temp) < self.num_applied_to:
                lowerb *= .9
                upperb *= 1.1
                if self.verbose:
                    print('Applicant ' + str(sel.name) + ' increased ' + 'applied_to_range')
            elif len(temp) == self.num_applied_to:
                self.applied_to = temp
            else:
                # TODO: should this list be sorted and then selected from in order?
                self.applied_to = r.sample(temp, self.num_applied_to)  # Randomly choose from the acceptable list
        for inst in self.applied_to:
            # TODO: need to test these cross class updates
            inst.applied.append(self)
        assert len(self.applied_to) >= self.num_applied_to, 'len(self.applied_to) >= self.num_applied_to'

    def rank_interviewed_inst(self, instlist):
        """ Choose to rank in consideration of interview """
        if len(instlist) == 0:
            self.failed_to_match = True
        lowerb = self.quality * self.applied_to_range[0]  # only exlude from ranking based on lower bound
        while (len(self.rank_inst) < self.num_to_rank) and not self.failed_to_match:
            for inst in instlist:
                observed_quality = inst.quality * inst.observed_1 * inst.observed_2 * self.observe  # elf.observe could be random or other non constant
                if observed_quality >= lowerb:
                    self.rank_inst.append(inst)
                else:
                    self.not_rank_inst.append(inst)
                assert (inst in self.not_rank_inst) or (inst in self.rank_inst), '(inst in self.not_rank_inst) or (inst in self.rank_inst)'
            if len(self.rank_inst) < self.num_to_rank:
                if self.verbose:
                    print('Applicant ' + str(self.name) + ' lowered rank expectation from' + str(lowerb) + ' to' + str(lowerb * .9))
                if lowerb < .00000000001:
                    self.failed_to_match = True
                lowerb *= .9  # Lower the expectations of the applicant
        assert (len(self.rank_inst) >= self.num_to_rank or self.failed_to_match), 'It should not be that len(app.rank_inst) >= self.num_to_rank ' + str(self.name)

    def sort_rank_interviewed_inst(self):
        # TOD0: Need a better name, for this method, maybe should be part of rank_interviewed_inst
        """
        Sorts the list of institutions that where chosen to rank.
        This is then the rank order.
        There is no strategy always rank by observed quality.
        List index position 0 is the best ranked
        don't worry about ties
        """

        # TODO: Need to check the sort order
        def make_key(inst):
            return inst.quality * inst.observed_1 * inst.observed_2

        self.rank_inst.sort(key=make_key, reverse=True)
        # self.try_inst = [x for x in self.rank_inst] #used for the match
