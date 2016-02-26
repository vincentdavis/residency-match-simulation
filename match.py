class Match(object):
    def __init__(self, applicant_list, institution_list, verbose=False):
        self.app_list = applicant_list
        self.inst_list = institution_list
        self.verbose = verbose

    def Applicant_not_matched(self):
        """
        Get a list of unmatched applicants that still have a chance to match.
        applicant.matched_to = None
        applicant.try_inst has institutions in it.
        applicant.failed_to_match does not = 1 or is not true
        if len(self.not_matched) == 0 then the match is complete
        """
        return [app for app in self.app_list if all([not (app.failed_to_match),
                                                     app.Institution_to_try_next() != None,
                                                     app.matched_to == None])]

    def run_match(self):
        while len(self.Applicant_not_matched()) > 0:
            if self.verbose:
                print('The number of appllicants which are not match but still have a chance is ' + str(len(self.Applicant_not_matched())))
            for app in self.Applicant_not_matched():
                assert app.matched_to == None, 'app.matched_to == None'
                inst = app.Institution_to_try_next()
                assert inst in app.rank_inst, 'inst in app.rank_inst'
                matching = inst.Proposed_applicant(app)  # returns [(true/false, app bumped(if)]
                if matching[0]:
                    app.matched_to = inst
                    if matching[1] != None:
                        bumped_app = matching[1]
                        print('inst', type(inst))
                        print('bumped_app.matched_to.name', type(bumped_app.matched_to))
                        print(bumped_app.matched_to.name, inst.name)
                        assert bumped_app.matched_to.name == inst.name, 'bumped_app.matched_to.name==inst.name'
                        bumped_app.not_matched_to.append(inst)
                        bumped_app.matched_to = None
                else:
                    assert matching[0] == False, 'matching[0] == False'
                    app.not_matched_to.append(inst)
                    assert app.matched_to == None, 'app.matched_to==None'
            print(('The number of appllicants which are not match but still have a chance is',
                   len(self.Applicant_not_matched())))
