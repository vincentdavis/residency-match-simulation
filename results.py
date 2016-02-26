from matplotlib import pyplot
from pylab import show
import numpy as np


class StatsAndplots(object):
    def __init__(self, all_applicants, all_institutions):
        self.all_applicants = all_applicants
        self.all_institutions = all_institutions

    def stats(self):
        #### Applicants

        number_matched = len([x for x in self.all_applicants if x.matched_to])
        # print('Number of applicants that matched', number_matched, [x for x in self.all_applicants if x.matched_to])
        number_not_matched = len([x for x in self.all_applicants if x.matched_to == None])
        print('number of applicants that did not match', number_not_matched)
        percentage = float(number_matched) / (number_matched + number_not_matched)
        print('Percentage of applicants that matched', percentage * 100)

        #### Average score of match, not matched
        app_mean_quality_matched = np.average([x.quality for x in self.all_applicants if x.matched_to])
        print('Average quality of the applicants that matched', app_mean_quality_matched)
        app_mean_quality_not_matched = np.average([x.quality for x in self.all_applicants if not x.matched_to])
        print('Average quality of the applicants that did not match', app_mean_quality_not_matched)
        app_mean_quality = np.average([x.quality for x in self.all_applicants])
        print('Average quality of all applicants', app_mean_quality)
        mean_app_inst_ratio = np.average([x.quality / x.matched_to.quality for x in self.all_applicants if x.matched_to])
        print('Average quality ratio of matched applicants / matched institution quality', mean_app_inst_ratio)

        #### Institutions
        num_filled = len([x for x in self.all_institutions if len(x.matched_to) == x.openings])
        print('Number of filled institutions', num_filled)
        num_not_filled = len([x for x in self.all_institutions if len(x.matched_to) != x.openings])
        print('Number of unfilled institutions', num_not_filled)
        inst_mean_quality_matched = np.average([x.quality for x in self.all_institutions if len(x.matched_to) == x.openings])
        print('Average quality of filled institutions', inst_mean_quality_matched)
        inst_mean_quality_not_matched = np.average([x.quality for x in self.all_institutions if len(x.matched_to) != x.openings])
        print('Average quality of unfilled institutions', inst_mean_quality_not_matched)

    #### plots
    def plots(self):
        def make_key(inst):
            return inst.quality

        self.all_institutions.sort(key=make_key, reverse=1)
        self.all_applicants.sort(key=make_key, reverse=1)

        print('histogram of institution quality for filled institutions')
        pyplot.hist([np.average([y.quality for y in x.matched_to]) for x in self.all_institutions], bins=20)
        show()
        print('histogram of institution quality for unfilled institutions')
        pyplot.hist([x.quality for x in self.all_institutions if len(x.matched_to) != x.openings], bins=20)
        show()
        print('Plot of')
        pyplot.plot([x.quality for x in self.all_institutions if len(x.matched_to) == x.openings],
                    [np.average([y.quality for y in x.matched_to]) for x in self.all_institutions if len(x.matched_to) == x.openings])
        show()
        pyplot.plot([x.quality for x in self.all_institutions if len(x.matched_to) == x.openings],
                    [np.min([y.quality for y in x.matched_to]) for x in self.all_institutions if len(x.matched_to) == x.openings])
        show()
        pyplot.plot([x.quality for x in self.all_institutions if len(x.matched_to) == x.openings],
                    [np.max([y.quality for y in x.matched_to]) for x in self.all_institutions if len(x.matched_to) == x.openings])
        show()
        pyplot.plot([x.quality for x in self.all_institutions], [np.average([y.quality for y in x.matched_to]) for x in self.all_institutions])
        show()

##        for x in self.all_institutions:
##            pyplot.boxplot([y.quality for y in x.matched_to])

##        pyplot.boxplot([[y.quality for y in x.matched_to] for x in self.all_institutions if len(x.matched_to) == x.openings])
